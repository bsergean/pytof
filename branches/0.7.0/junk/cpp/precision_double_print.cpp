
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// sh jmake precision_double_print.cpp ; cp ./precision_double_print ~/sandbox/ ; ~/sandbox/precision_double_print

// Units ratio conversion
#define RATIO_UNDEFINED 0.0f
#define RATIO_MM	 1.0f/1000.0f					//Millimeters
//#define RATIO_MIC	 RATIO_MM/1000.0f	//Micrometers
#define RATIO_MIC	 0.000001f	//Micrometers
#define RATIO_CM	 1.0f/100.0f					//Centimeters
#define RATIO_M	 1.0f							//Meters
#define RATIO_INCH	 0.0254f						//Inches
#define RATIO_FEET	 0.3048f	

int main()
{
  float units[] = {
    RATIO_UNDEFINED,
    RATIO_MM,
    RATIO_MIC,
    RATIO_CM,
    RATIO_M,
    RATIO_INCH,
    RATIO_FEET
  };
  const int nb_units = sizeof(units) / sizeof(float);

  int i;
  for (i = 0 ; i < nb_units ; i++)
    {
      char unit[200];
      int float_size = sprintf(unit, "%g", units[i]);
      printf("Unit written: %s\n", unit);
      
      double parsed = atof(unit);
      printf("Unit parsed: %g\n", parsed);
    }
  return 0;
}
