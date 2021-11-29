package util;

import java.util.EnumMap;

public abstract class Condition <T> implements AttributeMatcher<T>
{
    public enum Conjunction { AND, OR };
    public enum Operator { EQUALS, LESS_THAN, GREATER_THAN };
    private final EnumMap<Conjunction, AttributeMatcher<T>> attributeMatchers;
    private final Operator operator;

    public Condition(Operator operator)
    {
        this.operator = operator;
        attributeMatchers = new EnumMap<>(Conjunction.class);
    }

    public Condition<T> and(AttributeMatcher<T> attributeMatcher)
    {
        attributeMatchers.put(Conjunction.AND, attributeMatcher);
        return this;
    }

    public Condition<T> or(AttributeMatcher<T> attributeMatcher)
    {
        attributeMatchers.put(Conjunction.OR, attributeMatcher);
        return this;
    }

    public boolean evaluateSelf(int compare)
    {
        boolean rVal;
        switch(operator)
        {
            case EQUALS:
                rVal = compare == 0;
                break;
            case GREATER_THAN:
                rVal = compare > 0;
                break;
            case LESS_THAN:
                rVal = compare < 0;
                break;
            default:
                rVal = false;
                throw new RuntimeException("Error: Failed to find operator.");
        }
        return rVal;
    }

    public boolean evaluate(T t, boolean result)
    {
        if(result)
        {
            AttributeMatcher<T> andMatcher = attributeMatchers.get(Conjunction.AND);
            if(andMatcher != null)
            {
                if(!andMatcher.matching(t))
                {
                    result = false;
                }
            }
        }
        else
        {
            AttributeMatcher<T> orMatcher = attributeMatchers.get(Conjunction.OR);
            if(orMatcher != null)
            {
                if(orMatcher.matching(t))
                {
                    result = true;
                }
            }
        }
        return result;
    }
}
