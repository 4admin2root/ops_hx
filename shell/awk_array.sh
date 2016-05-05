awk -F "[:|]" '{ HV[int(($10-1458748770)/3600)]+=$16} END {for  (i  in  HV)  {print  i,HV[i]}}' /tmp/accounting.log
