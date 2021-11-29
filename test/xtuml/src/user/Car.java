package user;

import gen.classes._Car;

import java.awt.*;

public class Car extends _Car
{
    public Car(String licenseNumber, int color, int numberOfDoors)
    {
        setLicenseNumber(licenseNumber);
        setColor(color);
        setNumberOfDoors(numberOfDoors);
    }
}
