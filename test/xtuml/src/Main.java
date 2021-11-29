import gen.selectors.CarSelector;
import user.Car;
import user.Retailer;

import java.awt.*;

public class Main
{
    public static void main(String[] args)
    {
        Retailer retailer = new Retailer();
        retailer.relateAcrossR4(new Car("GJS-237", 2, 4));
        retailer.relateAcrossR4(new Car("ASD-192", 2, 2));
        retailer.relateAcrossR4(new Car("GHA-162", 2, 4));
        retailer.relateAcrossR4(new Car("WUZ-853", 3, 4));
        retailer.relateAcrossR4(new Car("GEH-813", 3, 2));
        retailer.relateAcrossR4(new Car("PPU-881", 4, 2));
        System.out.println("Look at this cool car: " + retailer.selectAnyAcrossR4(CarSelector.licenseNumber.equals("ASD-192")).getLicenseNumber());

        System.out.println("Cars with color 2:");
        for(Car car : retailer.selectManyAcrossR4(CarSelector.color.equals(2)))
        {
            System.out.println(car.getLicenseNumber());
        }
        Car carWithTwoDoors = retailer.selectAnyAcrossR4(CarSelector.color.equals(2).and(CarSelector.numberOfDoors.equals(2)));
        Retailer ret = carWithTwoDoors.selectOneAcrossR4();
        assert ret == retailer;
        System.out.println("Car with color 2 and 2 doors: " + carWithTwoDoors.getLicenseNumber());
        System.out.println("Cars with more than 2 doors or color greater than 3:");
        for(Car car : retailer.selectManyAcrossR4(CarSelector.numberOfDoors.greaterThan(2).or(CarSelector.color.greaterThan(3))))
        {
            System.out.println(car.getLicenseNumber());
        }
        System.out.println("Cars with (4 doors and color 3) or (color 2 and 2 doors):");
        for(Car car : retailer.selectManyAcrossR4((CarSelector.numberOfDoors.equals(4).and(CarSelector.color.equals(3)))
            .or((CarSelector.color.equals(2).and(CarSelector.numberOfDoors.equals(2))))))
        {
            System.out.println(car.getLicenseNumber());
        }
    }
}
