#pragma once

#include "primitives.h"

namespace {{packageName}}
{
    class {{className}}
    {
    public:
        {{className}}();

        virtual ~{{className}}() noexcept;

        [[attributes|void set{{attributeName:upperCC}}({{attributeType}} {{attributeName}})
        {
            _{{attributeName}} = {{attributeName}};
        }]]

        [[attributes|{{attributeType}} {{attributeName}}() const
        {
            return _{{attributeName}};
        }]]

    private:
        [[attributes|{{attributeType}} _{{attributeName}};]]
    };
}