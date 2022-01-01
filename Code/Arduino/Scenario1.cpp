/******************************************************************************
* Scenario1 -- OK, I'm an Arduino... 
*
******************************************************************************/


/******************************************************************************
*                                  MAIN
*
******************************************************************************/
int main(int argc, char **argv)
{
 string     myname("Freds FS1");
 string     myversion("0.0.1");

 PostMaster postoffice(myname);

 // My Constituent Parts - Use terse names!

 FS_IMU              ParallacticAngle("PA",postmaster); // default dispatch interval.
 FS_Blinky           Blinky("B",postmaster);            // Use defaults.
 FS_CamLinearFocuser Collimator("C",postmaster);        // the collimator
 FS_LimitedRotator   Grating("G",postmaster);           // TODO: What are the grating angles?
 FS_Switch           Backlight("BL",postmaster);        // The backlight LED


   postoffice.register(dynamic_cast<Patron *>(ParallacticAngle)); 
   postoffice.register(dynamic_cast<Patron *>(Blinky));
   postoffice.register(dynamic_cast<Patron *>(Collimator));
   postoffice.register(dynamic_cast<Patron *>(Backlight));

   postoffice.Open();      // FOREVER LOOP




   return 0;
} // main
