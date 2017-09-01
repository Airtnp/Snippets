module comparator(A, B, A_lt_B, A_eq_B, A_gt_B);
  parameter size = 3;
  input [size-1:0] A, B;
  output A_lt_B, A_eq_B, A_gt_B;
  
  assign A_lt_B = (A<B);
  assign A_eq_B = (A==B);
  assign A_gt_B = (A>B);

endmodule
