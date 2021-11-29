package util;

import java.util.ArrayList;
import java.util.Random;

public class RelationManager
{
    private static Random random = new Random(9874319241L);


    public static <T> ArrayList<T> selectMany(ArrayList<T> arrayList, AttributeMatcher<T> attributeMatcher)
    {
        ArrayList<T> matches = new ArrayList<>();
        for(T t : arrayList)
        {
            if(attributeMatcher.matching(t))
            {
                matches.add(t);
            }
        }
        return matches;
    }

    public static <T> T selectAny(ArrayList<T> arrayList, AttributeMatcher<T> attributeMatcher)
    {
        return selectAny(selectMany(arrayList, attributeMatcher));
    }

    public static <T> T selectAny(ArrayList<T> arrayList)
    {
        if(arrayList.size() == 0)
        {
            return null;
        }
        return arrayList.get(random.nextInt(arrayList.size()));
    }
}
