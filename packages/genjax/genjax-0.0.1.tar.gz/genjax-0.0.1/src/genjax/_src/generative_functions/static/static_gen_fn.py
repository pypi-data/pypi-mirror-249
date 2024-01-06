# Copyright 2023 MIT Probabilistic Computing Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
from dataclasses import dataclass

from genjax._src.core.datatypes.generative import (
    Choice,
    HierarchicalChoiceMap,
    JAXGenerativeFunction,
    Trace,
)
from genjax._src.core.interpreters.incremental import static_check_tree_leaves_diff
from genjax._src.core.pytree.closure import DynamicClosure
from genjax._src.core.typing import (
    Any,
    Callable,
    FloatArray,
    PRNGKey,
    Tuple,
    dispatch,
    typecheck,
)
from genjax._src.generative_functions.static.static_datatypes import StaticTrace
from genjax._src.generative_functions.static.static_transforms import (
    assess_transform,
    importance_transform,
    simulate_transform,
    trace,
    update_transform,
)
from genjax._src.generative_functions.supports_callees import (
    SupportsCalleeSugar,
    push_trace_overload_stack,
)

#######################
# Generative function #
#######################


# Callee syntactic sugar handler.
@typecheck
def handler_trace_with_static(
    addr,
    gen_fn: JAXGenerativeFunction,
    args: Tuple,
):
    return trace(addr, gen_fn)(*args)


@dataclass
class StaticGenerativeFunction(
    JAXGenerativeFunction,
    SupportsCalleeSugar,
):
    source: Callable

    def flatten(self):
        # NOTE: Experimental.
        if isinstance(self.source, DynamicClosure):
            return (self.source,), ()
        else:
            return (), (self.source,)

    @classmethod
    @typecheck
    def new(cls, source: Callable):
        gen_fn = StaticGenerativeFunction(source)
        functools.update_wrapper(gen_fn, source)
        return gen_fn

    # To get the type of return value, just invoke
    # the source (with abstract tracer arguments).
    def __abstract_call__(self, *args) -> Any:
        return self.source(*args)

    @typecheck
    def simulate(
        self,
        key: PRNGKey,
        args: Tuple,
    ) -> StaticTrace:
        syntax_sugar_handled = push_trace_overload_stack(
            handler_trace_with_static, self.source
        )
        (args, retval, address_choices, score), cache_state = simulate_transform(
            syntax_sugar_handled
        )(key, args)
        return StaticTrace.new(
            self,
            args,
            retval,
            address_choices,
            cache_state,
            score,
        )

    @dispatch
    def importance(
        self,
        key: PRNGKey,
        chm: Choice,
        args: Tuple,
    ) -> Tuple[StaticTrace, FloatArray]:
        syntax_sugar_handled = push_trace_overload_stack(
            handler_trace_with_static, self.source
        )
        (
            (
                w,
                (
                    args,
                    retval,
                    address_choices,
                    score,
                ),
            ),
            cache_state,
        ) = importance_transform(syntax_sugar_handled)(key, chm, args)
        return (
            StaticTrace.new(
                self,
                args,
                retval,
                address_choices,
                cache_state,
                score,
            ),
            w,
        )

    @dispatch
    def update(
        self,
        key: PRNGKey,
        prev: Trace,
        constraints: Choice,
        argdiffs: Tuple,
    ) -> Tuple[Trace, FloatArray, Any, Choice]:
        assert static_check_tree_leaves_diff(argdiffs)
        syntax_sugar_handled = push_trace_overload_stack(
            handler_trace_with_static, self.source
        )
        (
            (
                retval_diffs,
                weight,
                (
                    arg_primals,
                    retval_primals,
                    address_choices,
                    score,
                ),
                discard,
            ),
            cache_state,
        ) = update_transform(syntax_sugar_handled)(key, prev, constraints, argdiffs)
        return (
            StaticTrace.new(
                self,
                arg_primals,
                retval_primals,
                address_choices,
                cache_state,
                score,
            ),
            weight,
            retval_diffs,
            HierarchicalChoiceMap(discard),
        )

    @typecheck
    def assess(
        self,
        chm: Choice,
        args: Tuple,
    ) -> Tuple[FloatArray, Any]:
        syntax_sugar_handled = push_trace_overload_stack(
            handler_trace_with_static, self.source
        )
        (retval, score) = assess_transform(syntax_sugar_handled)(chm, args)
        return (score, retval)

    def inline(self, *args):
        return self.source(*args)

    def restore_with_aux(self, interface_data, aux):
        (original_args, retval, score, _) = interface_data
        (
            address_choices,
            cache,
        ) = aux
        return StaticTrace.new(
            self,
            original_args,
            retval,
            address_choices,
            cache,
            score,
        )

    ###################
    # Deserialization #
    ###################


##############################
# Partial binding / currying #
##############################


def partial(gen_fn, *static_args):
    return StaticGenerativeFunction.new(
        lambda *args: gen_fn.inline(*args, *static_args),
    )


#############
# Decorator #
#############


def Static(f) -> StaticGenerativeFunction:
    gf = StaticGenerativeFunction(f)
    functools.update_wrapper(gf, f)
    return gf
