module Top(clock, reset, valid, Data_in, RxReg_out);
  parameter size = 8;
  parameter counter_size = 3; 
  parameter comparator_const = 3'd6;
  
  input clock, reset, valid, Data_in;
  output [size-1:0] RxReg_out;

  wire A_lt_B, w_unused_1, w_unused_2, w_unused_3, counter_clr, CE, RxReg_ld;
  wire [counter_size-1:0] count;
  wire [size-1:0] RS_out;

  controller                    CTRL (clock, reset, valid, A_lt_B, CE, counter_clr, RxReg_ld);
  counter_N_bit #(counter_size) CNT  (clock, counter_clr, CE, count);
  comparator    #(counter_size) CMP  (count, comparator_const, A_lt_B, w_unused_1, w_unused_2);
  shift_reg     #(size)         SR   (RS_out, , Data_in, clock);
  Reg_N_bits    #(size)         REG  (RxReg_out, RS_out, clock, RxReg_ld);
  
endmodule
