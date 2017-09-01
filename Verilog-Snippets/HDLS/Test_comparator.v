module Test_comparator;
  parameter size = 3;
  
  reg [size-1:0] A, B;
  wire  A_lt_B, A_eq_B, A_gt_B;
  
  comparator UUT (A, B, A_lt_B, A_eq_B, A_gt_B);
  
  initial begin
    #0    A = 3; B = 6;
	 #100  A = 6; B = 6;
	 #100  A = 6; B = 3; 
	 #100  A = -3; B = 1;
  end
  

  initial #2000 $stop;
endmodule


