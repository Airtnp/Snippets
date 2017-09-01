module controller (clock, reset, valid, comp_out, count_en, count_clr, RxReg_ld);
  input 	clock, reset, valid, comp_out;
  output	count_en, count_clr, RxReg_ld;

  reg 		count_en, count_clr;
  reg [1:0]	curr_state, next_state;
  
  parameter Init 	= 2'b00;
  parameter Rec	= 2'b01;
  parameter Done	= 2'b10;

  always @(posedge clock or posedge reset)
    if (reset) 	curr_state <= Init;
    else			curr_state <= next_state;
  
  always @(curr_state or valid or comp_out)
    case (curr_state)
      Init: if (valid)    next_state <= Rec;
	         else          next_state <= Init;
      Rec:  if (comp_out) next_state <= Rec;
	         else          next_state <= Done;
      Done:               next_state <= Init;
      default:            next_state <= Init;
    endcase

  //Moore outputs
  always @(curr_state) 
  begin  
    count_en  = 0;
    count_clr = 0;
    case (curr_state)
      Init: count_clr = 1;
	   Rec:  count_en  = 1;
    endcase 
  end

  //Mealy outputs
  assign RxReg_ld = ((curr_state==Done)&&(comp_out==0)) ? 1 : 0;

endmodule
