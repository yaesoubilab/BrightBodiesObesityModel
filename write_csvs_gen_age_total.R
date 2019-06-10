obmod <- read.csv("Downloads/NLS1.csv")
step_data <- read.csv("Downloads/BMI_Percentile_byAgeSex.csv")

fem <- step_data[step_data$Sex == "F", ]
male <- step_data[step_data$Sex == "M", ]

#copy the obmod csv to another one so that we can see the difference 
obmodfin <- obmod

#Figuring out age 
obmodfin$age_1997 <- 1997 - obmodfin$Birthdate..Yr.
obmodfin$age_1998 <- 1998 - obmodfin$Birthdate..Yr.
obmodfin$age_1999 <- 1999 - obmodfin$Birthdate..Yr.
obmodfin$age_2000 <- 2000 - obmodfin$Birthdate..Yr.
obmodfin$age_2001 <- 2001 - obmodfin$Birthdate..Yr.
obmodfin$age_2002 <- 2002 - obmodfin$Birthdate..Yr.
obmodfin$age_2003 <- 2003 - obmodfin$Birthdate..Yr.
obmodfin$age_2004 <- 2004 - obmodfin$Birthdate..Yr.
obmodfin$age_2005 <- 2005 - obmodfin$Birthdate..Yr.
obmodfin$age_2006 <- 2006 - obmodfin$Birthdate..Yr.
obmodfin$age_2007 <- 2007 - obmodfin$Birthdate..Yr.
obmodfin$age_2008 <- 2008 - obmodfin$Birthdate..Yr.
obmodfin$age_2009 <- 2009 - obmodfin$Birthdate..Yr.
obmodfin$age_2010 <- 2010 - obmodfin$Birthdate..Yr.
obmodfin$age_2011 <- 2011 - obmodfin$Birthdate..Yr.
obmodfin$age_2013 <- 2013 - obmodfin$Birthdate..Yr.
obmodfin$age_2015 <- 2015 - obmodfin$Birthdate..Yr.

#converting feet to inches 
obmodfin$HT..ft..1997 <- obmodfin$HT..ft..1997 * 12
obmodfin$HT..ft..1998 <- obmodfin$HT..ft..1998 * 12
obmodfin$HT..ft..1999 <- obmodfin$HT..ft..1999 * 12
obmodfin$HT..ft..2000 <- obmodfin$HT..ft..2000 * 12
obmodfin$HT..ft..2001 <- obmodfin$HT..ft..2001 * 12
obmodfin$HT..ft..2002 <- obmodfin$HT..ft..2002 * 12
obmodfin$HT..ft..2003 <- obmodfin$HT..ft..2003 * 12
obmodfin$HT..ft..2004 <- obmodfin$HT..ft..2004 * 12
obmodfin$HT..ft..2005 <- obmodfin$HT..ft..2005 * 12
obmodfin$HT..ft..2006 <- obmodfin$HT..ft..2006 * 12
obmodfin$HT..ft..2007 <- obmodfin$HT..ft..2007 * 12
obmodfin$HT..ft..2008 <- obmodfin$HT..ft..2008 * 12
obmodfin$HT..ft..2009 <- obmodfin$HT..ft..2009 * 12
obmodfin$HT..ft..2010 <- obmodfin$HT..ft..2010 * 12
obmodfin$HT..ft..2011 <- obmodfin$HT..ft..2011 * 12

#convert to meters
obmodfin$height_meter_1997 <- (obmodfin$HT..ft..1997 + obmodfin$HT..in..1997) * 0.0254
obmodfin$height_meter_1998 <- (obmodfin$HT..ft..1998 + obmodfin$HT..in..1998) * 0.0254
obmodfin$height_meter_1999 <- (obmodfin$HT..ft..1999 + obmodfin$HT..in..1999) * 0.0254
obmodfin$height_meter_2000 <- (obmodfin$HT..ft..2000 + obmodfin$HT..in..2000) * 0.0254
obmodfin$height_meter_2001 <- (obmodfin$HT..ft..2001 + obmodfin$HT..in..2001) * 0.0254
obmodfin$height_meter_2002 <- (obmodfin$HT..ft..2002 + obmodfin$HT..in..2002) * 0.0254
obmodfin$height_meter_2003 <- (obmodfin$HT..ft..2003 + obmodfin$HT..in..2003) * 0.0254
obmodfin$height_meter_2004 <- (obmodfin$HT..ft..2004 + obmodfin$HT..in..2004) * 0.0254
obmodfin$height_meter_2005 <- (obmodfin$HT..ft..2005 + obmodfin$HT..in..2005) * 0.0254
obmodfin$height_meter_2006 <- (obmodfin$HT..ft..2006 + obmodfin$HT..in..2006) * 0.0254
obmodfin$height_meter_2007 <- (obmodfin$HT..ft..2007 + obmodfin$HT..in..2007) * 0.0254
obmodfin$height_meter_2008 <- (obmodfin$HT..ft..2008 + obmodfin$HT..in..2008) * 0.0254
obmodfin$height_meter_2009 <- (obmodfin$HT..ft..2009 + obmodfin$HT..in..2009) * 0.0254
obmodfin$height_meter_2010 <- (obmodfin$HT..ft..2010 + obmodfin$HT..in..2010) * 0.0254
obmodfin$height_meter_2011 <- (obmodfin$HT..ft..2011 + obmodfin$HT..in..2011) * 0.0254

#convert pounds to kilograms 
obmodfin$WT..lbs..1997 <- 0.453592 * obmodfin$WT..lbs..1997
obmodfin$WT..lbs..1998 <- 0.453592 * obmodfin$WT..lbs..1998
obmodfin$WT..lbs..1999 <- 0.453592 * obmodfin$WT..lbs..1999
obmodfin$WT..lbs..2000 <- 0.453592 * obmodfin$WT..lbs..2000
obmodfin$WT..lbs..2001 <- 0.453592 * obmodfin$WT..lbs..2001
obmodfin$WT..lbs..2002 <- 0.453592 * obmodfin$WT..lbs..2002
obmodfin$WT..lbs..2003 <- 0.453592 * obmodfin$WT..lbs..2003
obmodfin$WT..lbs..2004 <- 0.453592 * obmodfin$WT..lbs..2004
obmodfin$WT..lbs..2005 <- 0.453592 * obmodfin$WT..lbs..2005
obmodfin$WT..lbs..2006 <- 0.453592 * obmodfin$WT..lbs..2006
obmodfin$WT..lbs..2007 <- 0.453592 * obmodfin$WT..lbs..2007
obmodfin$WT..lbs..2008 <- 0.453592 * obmodfin$WT..lbs..2008
obmodfin$WT..lbs..2009 <- 0.453592 * obmodfin$WT..lbs..2009
obmodfin$WT..lbs..2010 <- 0.453592 * obmodfin$WT..lbs..2010
obmodfin$WT..lbs..2011 <- 0.453592 * obmodfin$WT..lbs..2011
obmodfin$WT..lbs..2013 <- 0.453592 * obmodfin$WT..lbs..2013
obmodfin$WT..lbs..2015 <- 0.453592 * obmodfin$WT..lbs..2015

#if either height or weight is negative then make sure to put NA so that you don't calculate it 
obmodfin$bmi_1997 <- obmodfin$WT..lbs..1997 / (obmodfin$height_meter_1997 * obmodfin$height_meter_1997)
obmodfin$bmi_1997[obmodfin$height_meter_1997 < 0 | obmodfin$WT..lbs..1997 < 0] <- NA
obmodfin$bmi_1998 <- obmodfin$WT..lbs..1998 / (obmodfin$height_meter_1998 * obmodfin$height_meter_1998)
obmodfin$bmi_1998[obmodfin$height_meter_1998 < 0 | obmodfin$WT..lbs..1998 < 0] <- NA
obmodfin$bmi_1999 <- obmodfin$WT..lbs..1999 / (obmodfin$height_meter_1999 * obmodfin$height_meter_1999)
obmodfin$bmi_1999[obmodfin$height_meter_1999 < 0 | obmodfin$WT..lbs..1999 < 0] <- NA
obmodfin$bmi_2000 <- obmodfin$WT..lbs..2000 / (obmodfin$height_meter_2000 * obmodfin$height_meter_2000)
obmodfin$bmi_2000[obmodfin$height_meter_2000 < 0 | obmodfin$WT..lbs..2000 < 0] <- NA
obmodfin$bmi_2001 <- obmodfin$WT..lbs..2001 / (obmodfin$height_meter_2001 * obmodfin$height_meter_2001)
obmodfin$bmi_2001[obmodfin$height_meter_2001 < 0 | obmodfin$WT..lbs..2001 < 0] <- NA
obmodfin$bmi_2002 <- obmodfin$WT..lbs..2002 / (obmodfin$height_meter_2002 * obmodfin$height_meter_2002)
obmodfin$bmi_2002[obmodfin$height_meter_2002 < 0 | obmodfin$WT..lbs..2002 < 0] <- NA
obmodfin$bmi_2003 <- obmodfin$WT..lbs..2003 / (obmodfin$height_meter_2003 * obmodfin$height_meter_2003)
obmodfin$bmi_2003[obmodfin$height_meter_2003 < 0 | obmodfin$WT..lbs..2003 < 0] <- NA
obmodfin$bmi_2004 <- obmodfin$WT..lbs..2004 / (obmodfin$height_meter_2004 * obmodfin$height_meter_2004)
obmodfin$bmi_2004[obmodfin$height_meter_2004 < 0 | obmodfin$WT..lbs..2004 < 0] <- NA
obmodfin$bmi_2005 <- obmodfin$WT..lbs..2005 / (obmodfin$height_meter_2005 * obmodfin$height_meter_2005)
obmodfin$bmi_2005[obmodfin$height_meter_2005 < 0 | obmodfin$WT..lbs..2005 < 0] <- NA
obmodfin$bmi_2006 <- obmodfin$WT..lbs..2006 / (obmodfin$height_meter_2006 * obmodfin$height_meter_2006)
obmodfin$bmi_2006[obmodfin$height_meter_2006 < 0 | obmodfin$WT..lbs..2006 < 0] <- NA
obmodfin$bmi_2007 <- obmodfin$WT..lbs..2007 / (obmodfin$height_meter_2007 * obmodfin$height_meter_2007)
obmodfin$bmi_2007[obmodfin$height_meter_2007 < 0 | obmodfin$WT..lbs..2007 < 0] <- NA
obmodfin$bmi_2008 <- obmodfin$WT..lbs..2008 / (obmodfin$height_meter_2008 * obmodfin$height_meter_2008)
obmodfin$bmi_2008[obmodfin$height_meter_2008 < 0 | obmodfin$WT..lbs..2008 < 0] <- NA
obmodfin$bmi_2009 <- obmodfin$WT..lbs..2009 / (obmodfin$height_meter_2009 * obmodfin$height_meter_2009)
obmodfin$bmi_2009[obmodfin$height_meter_2009 < 0 | obmodfin$WT..lbs..2009 < 0] <- NA
obmodfin$bmi_2010 <- obmodfin$WT..lbs..2010 / (obmodfin$height_meter_2010 * obmodfin$height_meter_2010)
obmodfin$bmi_2010[obmodfin$height_meter_2010 < 0 | obmodfin$WT..lbs..2010 < 0] <- NA
obmodfin$bmi_2011 <- obmodfin$WT..lbs..2011 / (obmodfin$height_meter_2011 * obmodfin$height_meter_2011)
obmodfin$bmi_2011[obmodfin$height_meter_2011 < 0 | obmodfin$WT..lbs..2011 < 0] <- NA

obmodfin <- na.omit(obmodfin)

write.csv(obmodfin, file = "ogdata.csv")

fem_start <- obmodfin[obmodfin$Sex == 2, ]
male_start <- obmodfin[obmodfin$Sex == 1, ]

age_13 <- obmodfin[obmodfin$age_1997 == 13, ]
age_14 <- obmodfin[obmodfin$age_1997 == 14, ]
age_15 <- obmodfin[obmodfin$age_1997 == 15, ]
age_16 <- obmodfin[obmodfin$age_1997 == 16, ]
age_17 <- obmodfin[obmodfin$age_1997 == 17, ]

age_13_f <- age_13[age_13$Sex == 2, ]
age_13_m <- age_13[age_13$Sex == 1, ]

age_14_f <- age_14[age_14$Sex == 2, ]
age_14_m <- age_14[age_14$Sex == 1, ]

age_15_f <- age_15[age_15$Sex == 2, ]
age_15_m <- age_15[age_15$Sex == 1, ]

age_16_f <- age_16[age_16$Sex == 2, ]
age_16_m <- age_16[age_16$Sex == 1, ]

age_17_f <- age_17[age_17$Sex == 2, ]
age_17_m <- age_17[age_17$Sex == 1, ]

#age 13 females
age_13_f_adj <- age_13_f[(age_13_f$bmi_1997 > 10 & age_13_f$bmi_1998 > 10 & 
                      age_13_f$bmi_1999 > 10 & age_13_f$bmi_2000 > 10 &
                      age_13_f$bmi_2001 > 10 & age_13_f$bmi_2002 > 10 &
                      age_13_f$bmi_2003 > 10 & age_13_f$bmi_2004 > 10 &
                      age_13_f$bmi_2005 > 10 & age_13_f$bmi_2006 > 10 & 
                      age_13_f$bmi_2007 > 10 & age_13_f$bmi_2008 > 10 &
                      age_13_f$bmi_2009 > 10 & age_13_f$bmi_2010 > 10 &
                      age_13_f$bmi_2011 > 10), ]

age_13_f_adj <- age_13_f_adj[(age_13_f_adj$bmi_1997 < 70| age_13_f_adj$bmi_1998 < 70 | 
                            age_13_f_adj$bmi_1999 < 70 | age_13_f_adj$bmi_2000 < 70 |
                            age_13_f_adj$bmi_2001 < 70 | age_13_f_adj$bmi_2002 < 70 |
                            age_13_f_adj$bmi_2003 < 70 | age_13_f_adj$bmi_2004 < 70 |
                            age_13_f_adj$bmi_2005 < 70 | age_13_f_adj$bmi_2006 < 70 | 
                            age_13_f_adj$bmi_2007 < 70 | age_13_f_adj$bmi_2008 < 70 |
                            age_13_f_adj$bmi_2009 < 70 | age_13_f_adj$bmi_2010 < 70 |
                            age_13_f_adj$bmi_2011 < 70), ]

age_13_f_adj <- age_13_f_adj[(age_13_f_adj$bmi_1997 > 26.2 | age_13_f_adj$bmi_1998 > 27.2 | age_13_f_adj$bmi_1999 > 28.1
                         | age_13_f_adj$bmi_2000 > 28.9 | age_13_f_adj$bmi_2001 > 29.6 | age_13_f_adj$bmi_2002 > 30.3
                         | age_13_f_adj$bmi_2003 > 31.0 | age_13_f_adj$bmi_2004 > 31.8 | age_13_f_adj$bmi_2005 > 30.0 
                         | age_13_f_adj$bmi_2006 > 30.0| age_13_f_adj$bmi_2007 > 30.0 | age_13_f_adj$bmi_2008 > 30.0 
                         | age_13_f_adj$bmi_2009 > 30.0 | age_13_f_adj$bmi_2010 > 30.0 | age_13_f_adj$bmi_2011 > 30.0), ]

#age 14 females
age_14_f_adj <- age_14_f[(age_14_f$bmi_1997 > 10 & age_14_f$bmi_1998 > 10 & 
                          age_14_f$bmi_1999 > 10 & age_14_f$bmi_2000 > 10 &
                          age_14_f$bmi_2001 > 10 & age_14_f$bmi_2002 > 10 &
                          age_14_f$bmi_2003 > 10 & age_14_f$bmi_2004 > 10 &
                          age_14_f$bmi_2005 > 10 & age_14_f$bmi_2006 > 10 & 
                          age_14_f$bmi_2007 > 10 & age_14_f$bmi_2008 > 10 &
                          age_14_f$bmi_2009 > 10 & age_14_f$bmi_2010 > 10 &
                          age_14_f$bmi_2011 > 10), ]

age_14_f_adj <- age_14_f_adj[(age_14_f_adj$bmi_1997 < 70| age_14_f_adj$bmi_1998 < 70 | 
                                age_14_f_adj$bmi_1999 < 70 | age_14_f_adj$bmi_2000 < 70 |
                                age_14_f_adj$bmi_2001 < 70 | age_14_f_adj$bmi_2002 < 70 |
                                age_14_f_adj$bmi_2003 < 70 | age_14_f_adj$bmi_2004 < 70 |
                                age_14_f_adj$bmi_2005 < 70 | age_14_f_adj$bmi_2006 < 70 | 
                                age_14_f_adj$bmi_2007 < 70 | age_14_f_adj$bmi_2008 < 70 |
                                age_14_f_adj$bmi_2009 < 70 | age_14_f_adj$bmi_2010 < 70 |
                                age_14_f_adj$bmi_2011 < 70), ]

age_14_f_adj <- age_14_f_adj[(age_14_f_adj$bmi_1997 > 27.2 | age_14_f_adj$bmi_1998 > 28.1 | age_14_f_adj$bmi_1999 > 28.9
                         | age_14_f_adj$bmi_2000 > 29.6 | age_14_f_adj$bmi_2001 > 30.3 | age_14_f_adj$bmi_2002 > 31
                         | age_14_f_adj$bmi_2003 > 31.8 | age_14_f_adj$bmi_2004 > 30 | age_14_f_adj$bmi_2005 > 30 
                         | age_14_f_adj$bmi_2006 > 30| age_14_f_adj$bmi_2007 > 30 | age_14_f_adj$bmi_2008 > 30 
                         | age_14_f_adj$bmi_2009 > 30 | age_14_f_adj$bmi_2010 > 30 | age_14_f_adj$bmi_2011 > 30), ]


#age 15 females
age_15_f_adj <- age_15_f[(age_15_f$bmi_1997 > 10 & age_15_f$bmi_1998 > 10 & 
                            age_15_f$bmi_1999 > 10 & age_15_f$bmi_2000 > 10 &
                            age_15_f$bmi_2001 > 10 & age_15_f$bmi_2002 > 10 &
                            age_15_f$bmi_2003 > 10 & age_15_f$bmi_2004 > 10 &
                            age_15_f$bmi_2005 > 10 & age_15_f$bmi_2006 > 10 & 
                            age_15_f$bmi_2007 > 10 & age_15_f$bmi_2008 > 10 &
                            age_15_f$bmi_2009 > 10 & age_15_f$bmi_2010 > 10 &
                            age_15_f$bmi_2011 > 10), ]

age_15_f_adj <- age_15_f_adj[(age_15_f_adj$bmi_1997 < 70| age_15_f_adj$bmi_1998 < 70 | 
                                age_15_f_adj$bmi_1999 < 70 | age_15_f_adj$bmi_2000 < 70 |
                                age_15_f_adj$bmi_2001 < 70 | age_15_f_adj$bmi_2002 < 70 |
                                age_15_f_adj$bmi_2003 < 70 | age_15_f_adj$bmi_2004 < 70 |
                                age_15_f_adj$bmi_2005 < 70 | age_15_f_adj$bmi_2006 < 70 | 
                                age_15_f_adj$bmi_2007 < 70 | age_15_f_adj$bmi_2008 < 70 |
                                age_15_f_adj$bmi_2009 < 70 | age_15_f_adj$bmi_2010 < 70 |
                                age_15_f_adj$bmi_2011 < 70), ]

age_15_f_adj <- age_15_f_adj[(age_15_f_adj$bmi_1997 > 28.1 | age_15_f_adj$bmi_1998 > 28.9 | age_15_f_adj$bmi_1999 > 29.6
                         | age_15_f_adj$bmi_2000 > 30.3 | age_15_f_adj$bmi_2001 > 31 | age_15_f_adj$bmi_2002 > 31.8
                         | age_15_f_adj$bmi_2003 > 30 | age_15_f_adj$bmi_2004 > 30 | age_15_f_adj$bmi_2005 > 30 
                         | age_15_f_adj$bmi_2006 > 30| age_15_f_adj$bmi_2007 > 30 | age_15_f_adj$bmi_2008 > 30 
                         | age_15_f_adj$bmi_2009 > 30 | age_15_f_adj$bmi_2010 > 30 | age_15_f_adj$bmi_2011 > 30), ]

#age 16 females
age_16_f_adj <- age_16_f[(age_16_f$bmi_1997 > 10 & age_16_f$bmi_1998 > 10 & 
                          age_16_f$bmi_1999 > 10 & age_16_f$bmi_2000 > 10 &
                          age_16_f$bmi_2001 > 10 & age_16_f$bmi_2002 > 10 &
                          age_16_f$bmi_2003 > 10 & age_16_f$bmi_2004 > 10 &
                          age_16_f$bmi_2005 > 10 & age_16_f$bmi_2006 > 10 & 
                          age_16_f$bmi_2007 > 10 & age_16_f$bmi_2008 > 10 &
                          age_16_f$bmi_2009 > 10 & age_16_f$bmi_2010 > 10 &
                          age_16_f$bmi_2011 > 10), ]

age_16_f_adj <- age_16_f_adj[(age_16_f_adj$bmi_1997 < 70| age_16_f_adj$bmi_1998 < 70 | 
                                age_16_f_adj$bmi_1999 < 70 | age_16_f_adj$bmi_2000 < 70 |
                                age_16_f_adj$bmi_2001 < 70 | age_16_f_adj$bmi_2002 < 70 |
                                age_16_f_adj$bmi_2003 < 70 | age_16_f_adj$bmi_2004 < 70 |
                                age_16_f_adj$bmi_2005 < 70 | age_16_f_adj$bmi_2006 < 70 | 
                                age_16_f_adj$bmi_2007 < 70 | age_16_f_adj$bmi_2008 < 70 |
                                age_16_f_adj$bmi_2009 < 70 | age_16_f_adj$bmi_2010 < 70 |
                                age_16_f_adj$bmi_2011 < 70), ]

age_16_f_adj <- age_16_f_adj[(age_16_f_adj$bmi_1997 > 28.9 | age_16_f_adj$bmi_1998 > 29.6 | age_16_f_adj$bmi_1999 > 30.3
                             | age_16_f_adj$bmi_2000 > 31 | age_16_f_adj$bmi_2001 > 31.8 | age_16_f_adj$bmi_2002 > 30
                             | age_16_f_adj$bmi_2003 > 30 | age_16_f_adj$bmi_2004 > 30 | age_16_f_adj$bmi_2005 > 30 
                             | age_16_f_adj$bmi_2006 > 30| age_16_f_adj$bmi_2007 > 30 | age_16_f_adj$bmi_2008 > 30 
                             | age_16_f_adj$bmi_2009 > 30 | age_16_f_adj$bmi_2010 > 30 | age_16_f_adj$bmi_2011 > 30), ]

#age 17 females
age_17_f_adj <- age_17_f[(age_17_f$bmi_1997 > 10 & age_17_f$bmi_1998 > 10 & 
                            age_17_f$bmi_1999 > 10 & age_17_f$bmi_2000 > 10 &
                            age_17_f$bmi_2001 > 10 & age_17_f$bmi_2002 > 10 &
                            age_17_f$bmi_2003 > 10 & age_17_f$bmi_2004 > 10 &
                            age_17_f$bmi_2005 > 10 & age_17_f$bmi_2006 > 10 & 
                            age_17_f$bmi_2007 > 10 & age_17_f$bmi_2008 > 10 &
                            age_17_f$bmi_2009 > 10 & age_17_f$bmi_2010 > 10 &
                            age_17_f$bmi_2011 > 10), ]

age_17_f_adj <- age_17_f_adj[(age_17_f_adj$bmi_1997 < 70| age_17_f_adj$bmi_1998 < 70 | 
                                age_17_f_adj$bmi_1999 < 70 | age_17_f_adj$bmi_2000 < 70 |
                                age_17_f_adj$bmi_2001 < 70 | age_17_f_adj$bmi_2002 < 70 |
                                age_17_f_adj$bmi_2003 < 70 | age_17_f_adj$bmi_2004 < 70 |
                                age_17_f_adj$bmi_2005 < 70 | age_17_f_adj$bmi_2006 < 70 | 
                                age_17_f_adj$bmi_2007 < 70 | age_17_f_adj$bmi_2008 < 70 |
                                age_17_f_adj$bmi_2009 < 70 | age_17_f_adj$bmi_2010 < 70 |
                                age_17_f_adj$bmi_2011 < 70), ]
age_17_f_adj <- age_17_f_adj[(age_17_f_adj$bmi_1997 > 29.6 | age_17_f_adj$bmi_1998 > 30.3 | age_17_f_adj$bmi_1999 > 31
                             | age_17_f_adj$bmi_2000 > 31.8 | age_17_f_adj$bmi_2001 > 30 | age_17_f_adj$bmi_2002 > 30
                             | age_17_f_adj$bmi_2003 > 30 | age_17_f_adj$bmi_2004 > 30 | age_17_f_adj$bmi_2005 > 30 
                             | age_17_f_adj$bmi_2006 > 30| age_17_f_adj$bmi_2007 > 30 | age_17_f_adj$bmi_2008 > 30 
                             | age_17_f_adj$bmi_2009 > 30 | age_17_f_adj$bmi_2010 > 30 | age_17_f_adj$bmi_2011 > 30), ]


#age 13 males
age_13_m_adj <- age_13_m[(age_13_m$bmi_1997 > 10 & age_13_m$bmi_1998 > 10 & 
                            age_13_m$bmi_1999 > 10 & age_13_m$bmi_2000 > 10 &
                            age_13_m$bmi_2001 > 10 & age_13_m$bmi_2002 > 10 &
                            age_13_m$bmi_2003 > 10 & age_13_m$bmi_2004 > 10 &
                            age_13_m$bmi_2005 > 10 & age_13_m$bmi_2006 > 10 & 
                            age_13_m$bmi_2007 > 10 & age_13_m$bmi_2008 > 10 &
                            age_13_m$bmi_2009 > 10 & age_13_m$bmi_2010 > 10 &
                            age_13_m$bmi_2011 > 10), ]

age_13_m_adj <- age_13_m_adj[(age_13_m_adj$bmi_1997 < 70| age_13_m_adj$bmi_1998 < 70 | 
                                age_13_m_adj$bmi_1999 < 70 | age_13_m_adj$bmi_2000 < 70 |
                                age_13_m_adj$bmi_2001 < 70 | age_13_m_adj$bmi_2002 < 70 |
                                age_13_m_adj$bmi_2003 < 70 | age_13_m_adj$bmi_2004 < 70 |
                                age_13_m_adj$bmi_2005 < 70 | age_13_m_adj$bmi_2006 < 70 | 
                                age_13_m_adj$bmi_2007 < 70 | age_13_m_adj$bmi_2008 < 70 |
                                age_13_m_adj$bmi_2009 < 70 | age_13_m_adj$bmi_2010 < 70 |
                                age_13_m_adj$bmi_2011 < 70), ]

age_13_m_adj <- age_13_m_adj[(age_13_m_adj$bmi_1997 > 25.2 | age_13_m_adj$bmi_1998 > 26.0 | age_13_m_adj$bmi_1999 > 26.8
                             | age_13_m_adj$bmi_2000 > 27.5 | age_13_m_adj$bmi_2001 > 28.2 | age_13_m_adj$bmi_2002 > 28.9
                             | age_13_m_adj$bmi_2003 > 29.7 | age_13_m_adj$bmi_2004 > 30.6 | age_13_m_adj$bmi_2005 > 30.0 
                             | age_13_m_adj$bmi_2006 > 30.0| age_13_m_adj$bmi_2007 > 30.0 | age_13_m_adj$bmi_2008 > 30.0 
                             | age_13_m_adj$bmi_2009 > 30.0 | age_13_m_adj$bmi_2010 > 30.0 | age_13_m_adj$bmi_2011 > 30.0), ]

#age 14 males
age_14_m_adj <- age_14_m[(age_14_m$bmi_1997 > 10 & age_14_m$bmi_1998 > 10 & 
                            age_14_m$bmi_1999 > 10 & age_14_m$bmi_2000 > 10 &
                            age_14_m$bmi_2001 > 10 & age_14_m$bmi_2002 > 10 &
                            age_14_m$bmi_2003 > 10 & age_14_m$bmi_2004 > 10 &
                            age_14_m$bmi_2005 > 10 & age_14_m$bmi_2006 > 10 & 
                            age_14_m$bmi_2007 > 10 & age_14_m$bmi_2008 > 10 &
                            age_14_m$bmi_2009 > 10 & age_14_m$bmi_2010 > 10 &
                            age_14_m$bmi_2011 > 10), ]

age_14_m_adj <- age_14_m_adj[(age_14_m_adj$bmi_1997 < 70| age_14_m_adj$bmi_1998 < 70 | 
                                age_14_m_adj$bmi_1999 < 70 | age_14_m_adj$bmi_2000 < 70 |
                                age_14_m_adj$bmi_2001 < 70 | age_14_m_adj$bmi_2002 < 70 |
                                age_14_m_adj$bmi_2003 < 70 | age_14_m_adj$bmi_2004 < 70 |
                                age_14_m_adj$bmi_2005 < 70 | age_14_m_adj$bmi_2006 < 70 | 
                                age_14_m_adj$bmi_2007 < 70 | age_14_m_adj$bmi_2008 < 70 |
                                age_14_m_adj$bmi_2009 < 70 | age_14_m_adj$bmi_2010 < 70 |
                                age_14_m_adj$bmi_2011 < 70), ]

age_14_m_adj <- age_14_m_adj[(age_14_m_adj$bmi_1997 > 26.0 | age_14_m_adj$bmi_1998 > 26.8 | age_14_m_adj$bmi_1999 > 27.5
                             | age_14_m_adj$bmi_2000 > 28.2 | age_14_m_adj$bmi_2001 > 28.9 | age_14_m_adj$bmi_2002 > 29.7
                             | age_14_m_adj$bmi_2003 > 30.6 | age_14_m_adj$bmi_2004 > 30 | age_14_m_adj$bmi_2005 > 30 
                             | age_14_m_adj$bmi_2006 > 30| age_14_m_adj$bmi_2007 > 30 | age_14_m_adj$bmi_2008 > 30 
                             | age_14_m_adj$bmi_2009 > 30 | age_14_m_adj$bmi_2010 > 30 | age_14_m_adj$bmi_2011 > 30), ]


#age 15 males
age_15_m_adj <- age_15_m[(age_15_m$bmi_1997 > 10 & age_15_m$bmi_1998 > 10 & 
                            age_15_m$bmi_1999 > 10 & age_15_m$bmi_2000 > 10 &
                            age_15_m$bmi_2001 > 10 & age_15_m$bmi_2002 > 10 &
                            age_15_m$bmi_2003 > 10 & age_15_m$bmi_2004 > 10 &
                            age_15_m$bmi_2005 > 10 & age_15_m$bmi_2006 > 10 & 
                            age_15_m$bmi_2007 > 10 & age_15_m$bmi_2008 > 10 &
                            age_15_m$bmi_2009 > 10 & age_15_m$bmi_2010 > 10 &
                            age_15_m$bmi_2011 > 10), ]

age_15_m_adj <- age_15_m_adj[(age_15_m_adj$bmi_1997 < 70| age_15_m_adj$bmi_1998 < 70 | 
                                age_15_m_adj$bmi_1999 < 70 | age_15_m_adj$bmi_2000 < 70 |
                                age_15_m_adj$bmi_2001 < 70 | age_15_m_adj$bmi_2002 < 70 |
                                age_15_m_adj$bmi_2003 < 70 | age_15_m_adj$bmi_2004 < 70 |
                                age_15_m_adj$bmi_2005 < 70 | age_15_m_adj$bmi_2006 < 70 | 
                                age_15_m_adj$bmi_2007 < 70 | age_15_m_adj$bmi_2008 < 70 |
                                age_15_m_adj$bmi_2009 < 70 | age_15_m_adj$bmi_2010 < 70 |
                                age_15_m_adj$bmi_2011 < 70), ]

age_15_m_adj <- age_15_m_adj[(age_15_m_adj$bmi_1997 > 26.8 | age_15_m_adj$bmi_1998 > 27.5 | age_15_m_adj$bmi_1999 > 28.2
                             | age_15_m_adj$bmi_2000 > 28.9 | age_15_m_adj$bmi_2001 > 29.7 | age_15_m_adj$bmi_2002 > 30.6
                             | age_15_m_adj$bmi_2003 > 30 | age_15_m_adj$bmi_2004 > 30 | age_15_m_adj$bmi_2005 > 30 
                             | age_15_m_adj$bmi_2006 > 30| age_15_m_adj$bmi_2007 > 30 | age_15_m_adj$bmi_2008 > 30 
                             | age_15_m_adj$bmi_2009 > 30 | age_15_m_adj$bmi_2010 > 30 | age_15_m_adj$bmi_2011 > 30), ]

#age 16 males

age_16_m_adj <- age_16_m[(age_16_m$bmi_1997 > 10 & age_16_m$bmi_1998 > 10 & 
                            age_16_m$bmi_1999 > 10 & age_16_m$bmi_2000 > 10 &
                            age_16_m$bmi_2001 > 10 & age_16_m$bmi_2002 > 10 &
                            age_16_m$bmi_2003 > 10 & age_16_m$bmi_2004 > 10 &
                            age_16_m$bmi_2005 > 10 & age_16_m$bmi_2006 > 10 & 
                            age_16_m$bmi_2007 > 10 & age_16_m$bmi_2008 > 10 &
                            age_16_m$bmi_2009 > 10 & age_16_m$bmi_2010 > 10 &
                            age_16_m$bmi_2011 > 10), ]

age_16_m_adj <- age_16_m_adj[(age_16_m_adj$bmi_1997 < 70| age_16_m_adj$bmi_1998 < 70 | 
                                age_16_m_adj$bmi_1999 < 70 | age_16_m_adj$bmi_2000 < 70 |
                                age_16_m_adj$bmi_2001 < 70 | age_16_m_adj$bmi_2002 < 70 |
                                age_16_m_adj$bmi_2003 < 70 | age_16_m_adj$bmi_2004 < 70 |
                                age_16_m_adj$bmi_2005 < 70 | age_16_m_adj$bmi_2006 < 70 | 
                                age_16_m_adj$bmi_2007 < 70 | age_16_m_adj$bmi_2008 < 70 |
                                age_16_m_adj$bmi_2009 < 70 | age_16_m_adj$bmi_2010 < 70 |
                                age_16_m_adj$bmi_2011 < 70), ]

age_16_m_adj <- age_16_m_adj[(age_16_m_adj$bmi_1997 > 27.5 | age_16_m_adj$bmi_1998 > 28.2 | age_16_m_adj$bmi_1999 > 28.9
                             | age_16_m_adj$bmi_2000 > 29.7 | age_16_m_adj$bmi_2001 > 30.6 | age_16_m_adj$bmi_2002 > 30
                             | age_16_m_adj$bmi_2003 > 30 | age_16_m_adj$bmi_2004 > 30 | age_16_m_adj$bmi_2005 > 30 
                             | age_16_m_adj$bmi_2006 > 30| age_16_m_adj$bmi_2007 > 30 | age_16_m_adj$bmi_2008 > 30 
                             | age_16_m_adj$bmi_2009 > 30 | age_16_m_adj$bmi_2010 > 30 | age_16_m_adj$bmi_2011 > 30), ]

#age 17 males
age_17_m_adj <- age_17_m[(age_17_m$bmi_1997 > 10 & age_17_m$bmi_1998 > 10 & 
                            age_17_m$bmi_1999 > 10 & age_17_m$bmi_2000 > 10 &
                            age_17_m$bmi_2001 > 10 & age_17_m$bmi_2002 > 10 &
                            age_17_m$bmi_2003 > 10 & age_17_m$bmi_2004 > 10 &
                            age_17_m$bmi_2005 > 10 & age_17_m$bmi_2006 > 10 & 
                            age_17_m$bmi_2007 > 10 & age_17_m$bmi_2008 > 10 &
                            age_17_m$bmi_2009 > 10 & age_17_m$bmi_2010 > 10 &
                            age_17_m$bmi_2011 > 10), ]

age_17_m_adj <- age_17_m_adj[(age_17_m_adj$bmi_1997 < 70| age_17_m_adj$bmi_1998 < 70 | 
                                age_17_m_adj$bmi_1999 < 70 | age_17_m_adj$bmi_2000 < 70 |
                                age_17_m_adj$bmi_2001 < 70 | age_17_m_adj$bmi_2002 < 70 |
                                age_17_m_adj$bmi_2003 < 70 | age_17_m_adj$bmi_2004 < 70 |
                                age_17_m_adj$bmi_2005 < 70 | age_17_m_adj$bmi_2006 < 70 | 
                                age_17_m_adj$bmi_2007 < 70 | age_17_m_adj$bmi_2008 < 70 |
                                age_17_m_adj$bmi_2009 < 70 | age_17_m_adj$bmi_2010 < 70 |
                                age_17_m_adj$bmi_2011 < 70), ]
age_17_m_adj <- age_17_m_adj[(age_17_m_adj$bmi_1997 > 28.2 | age_17_m_adj$bmi_1998 > 28.9 | age_17_m_adj$bmi_1999 > 29.7
                             | age_17_m_adj$bmi_2000 > 30.6 | age_17_m_adj$bmi_2001 > 30 | age_17_m_adj$bmi_2002 > 30
                             | age_17_m_adj$bmi_2003 > 30 | age_17_m_adj$bmi_2004 > 30 | age_17_m_adj$bmi_2005 > 30 
                             | age_17_m_adj$bmi_2006 > 30| age_17_m_adj$bmi_2007 > 30 | age_17_m_adj$bmi_2008 > 30 
                             | age_17_m_adj$bmi_2009 > 30 | age_17_m_adj$bmi_2010 > 30 | age_17_m_adj$bmi_2011 > 30), ]

write.csv(age_13_f_adj, file = "age_13_females.csv")
write.csv(age_14_f_adj, file = "age_14_females.csv")
write.csv(age_15_f_adj, file = "age_15_females.csv")
write.csv(age_16_f_adj, file = "age_16_females.csv")
write.csv(age_17_f_adj, file = "age_17_females.csv")
write.csv(age_13_m_adj, file = "age_13_males.csv")
write.csv(age_14_m_adj, file = "age_14_males.csv")
write.csv(age_15_m_adj, file = "age_15_males.csv")
write.csv(age_16_m_adj, file = "age_16_males.csv")
write.csv(age_17_m_adj, file = "age_17_males.csv")

bmi_13_f_temp <- age_13_f_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_13_f_temp <- age_13_f_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_14_f_temp <- age_14_f_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_14_f_temp <- age_14_f_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_15_f_temp <- age_15_f_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_15_f_temp <- age_15_f_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_16_f_temp <- age_16_f_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_16_f_temp <- age_16_f_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_17_f_temp <- age_17_f_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_17_f_temp <- age_17_f_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_13_m_temp <- age_13_m_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_13_m_temp <- age_13_m_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_14_m_temp <- age_14_m_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_14_m_temp <- age_14_m_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_15_m_temp <- age_15_m_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_15_m_temp <- age_15_m_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_16_m_temp <- age_16_m_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_16_m_temp <- age_16_m_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

bmi_17_m_temp <- age_17_m_adj[,c("bmi_1997", "bmi_1998", "bmi_1999", "bmi_2000", "bmi_2001", "bmi_2002", "bmi_2003", "bmi_2004", "bmi_2005", "bmi_2006", "bmi_2007", "bmi_2008", "bmi_2009", "bmi_2010", "bmi_2011")]
age_17_m_temp <- age_17_m_adj[, c("age_1997", "age_1998", "age_1999", "age_2000", "age_2001", "age_2002", "age_2003", "age_2004", "age_2005", "age_2006", "age_2007", "age_2008", "age_2009", "age_2010", "age_2011")]

pdf('genoverplot.pdf')
plot.default(age_13_f_temp[1, ], bmi_13_f_temp[1, ], type = "l", main = "Trajectory of BMI exceeding Threshold with Age", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_13_f_temp)[1])){
  par(new = TRUE)
  plot.default(age_13_f_temp[i, ], bmi_13_f_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_14_f_temp[1, ], bmi_14_f_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_14_f_temp)[1])){
  par(new = TRUE)
  plot.default(age_14_f_temp[i, ], bmi_14_f_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_15_f_temp[1, ], bmi_15_f_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_15_f_temp)[1])){
  par(new = TRUE)
  plot.default(age_15_f_temp[i, ], bmi_15_f_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_16_f_temp[1, ], bmi_16_f_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_16_f_temp)[1])){
  par(new = TRUE)
  plot.default(age_16_f_temp[i, ], bmi_16_f_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_17_f_temp[1, ], bmi_17_f_temp[1, ], type = "l",xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_17_f_temp)[1])){
  par(new = TRUE)
  plot.default(age_17_f_temp[i, ], bmi_17_f_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_13_m_temp[1, ], bmi_13_m_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_13_m_temp)[1])){
  par(new = TRUE)
  plot.default(age_13_m_temp[i, ], bmi_13_m_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_14_m_temp[1, ], bmi_14_m_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_14_m_temp)[1])){
  par(new = TRUE)
  plot.default(age_14_m_temp[i, ], bmi_14_m_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_15_m_temp[1, ], bmi_15_m_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_15_m_temp)[1])){
  par(new = TRUE)
  plot.default(age_15_m_temp[i, ], bmi_15_m_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_16_m_temp[1, ], bmi_16_m_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_16_m_temp)[1])){
  par(new = TRUE)
  plot.default(age_16_m_temp[i, ], bmi_16_m_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot.default(age_17_m_temp[1, ], bmi_17_m_temp[1, ], type = "l", xlab = "Age", ylab = "BMI", xlim = c(12, 32), ylim = c(0, 230), lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
for (i in c(2:dim(bmi_17_m_temp)[1])){
  par(new = TRUE)
  plot.default(age_17_m_temp[i, ], bmi_17_m_temp[i, ], type = "l", xlim = c(12, 32), ylim = c(0, 230), xlab = "Age", ylab = "BMI", lwd = 0.5, col = rgb(0, 0, 0, alpha = 0.3))
}
par(new = TRUE)
plot(fem$Age,fem$BMI...95th..ile, xlim = c(12, 32), ylim = c(0, 230), type = "s", col = "cyan", xlab = "", ylab = "")
par(new = TRUE)
plot(male$Age,male$BMI...95th..ile, xlim = c(12, 32), ylim = c(0, 230), type = "s", col = "blue", xlab = "", ylab = "")
legend("topright", inset=.02, title="BMI By Gender",
       c("Male","Female"), fill=topo.colors(2), cex = 0.8)
dev.off()


write.csv(bmi_13_f_temp, file = "f_13.csv")
write.csv(bmi_14_f_temp, file = "f_14.csv")
write.csv(bmi_15_f_temp, file = "f_15.csv")
write.csv(bmi_16_f_temp, file = "f_16.csv")
write.csv(bmi_17_f_temp, file = "f_17.csv")

write.csv(bmi_13_m_temp, file = "m_13.csv")
write.csv(bmi_14_m_temp, file = "m_14.csv")
write.csv(bmi_15_m_temp, file = "m_15.csv")
write.csv(bmi_16_m_temp, file = "m_16.csv")
write.csv(bmi_17_m_temp, file = "m_17.csv")
