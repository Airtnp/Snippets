module SyncCounter/*WithAsyncResetSyncSet*/(out,set,clear,clock);
    parameter N = 4;
    input set,clear,clock;
    output reg [N - 1:0] out=4'b0000;
    always @ (posedge clear or posedge clock) begin
        if (clear == 1'b1) out <= 0;
        else if (set == 1'b1) out <= out+1;
        else out <= out-1;
    end
endmodule

module SyncCounterWithCE(clk, reset, load, CE, D, Q, CEO);
    parameter N = 4;
    input clk, reset, load, CE;
    input [N-1:0] D;
    output reg [N-1:0] Q;
    output CEO;

    assign CEO = CE & (&Q);

    always @ (posedge reset or posedge clk) begin
        if (reset == 1'b1) Q <= 0;
        else if (load == 1'b1) Q <= D;
        else if (CE == 1'b1) Q <= Q + 1;
        else Q <= Q;
    end
endmodule


module SSD(num,c);
	input [3:0] num;
	output reg [6:0] c;

	always @ * begin
		case(num)
			4'b0000: c<=7'b1000000;
			4'b0001: c<=7'b1111001;
			4'b0010: c<=7'b0100100;
			4'b0011: c<=7'b0110000;
			4'b0100: c<=7'b0011001;
			4'b0101: c<=7'b0010010;
			4'b0110: c<=7'b0000010;
			4'b0111: c<=7'b1111000;
			4'b1000: c<=7'b0000000;
			4'b1001: c<=7'b0010000;
			4'b1010: c<=7'b0001000;
			4'b1011: c<=7'b0000011;
			4'b1100: c<=7'b1000110;
			4'b1101: c<=7'b0100001;
			4'b1110: c<=7'b0000110;
			default: c<=7'b0001110;
		endcase
	end
endmodule

module HalfAdder(a, b, cout, sum);
    input a, b;
    output cout, sum;

    wire coutbar;

    xor(sum, a, b);
    nand(coutbar, a, b);
    not(cout, coutbar);
endmodule;

module FullAdder(a, b, cin, cout, sum);
    input a, b, cin;
    output cout, sum;
    wire ccout, csum, cccout;

    HalfAdder HA1(a, b, ccout, csum);
    HalfAdder HA2(cin, csum, cccout, sum);

    or(cout, cccout, ccout);
endmodule

module CarryRippleAdder(a, b, cin, cout, sum);
    input [3:0] a, b
    input cin;
    output [3:0] sum;
    output cout;

    wire cin2, cin3, cin4;
    FullAdder FA0(a[0], b[0], cin, cin2, sum[0]);
    FullAdder FA1(a[1], b[1], cin2, cin3, sum[1]);
    FullAdder FA2(a[2], b[2], cin3, cin4, sum[2]);
    FullAdder FA3(a[3], b[3], cin4, cout, sum[3]);
endmodule
    
module RTLAdder(a, b, cin, cout, sum, overflow);
    parameter N = 16;
    input [N-1:0] a, b;
    input cin;
    output [N-1:0] sum;
    output cout, overflow;
	wire lcout;
	wire [N-2:0] lsum;

    assign {cout, sum} = a + b + cin;
	assign {lcout, lsum} = a[N-2:0] + b[N-2:0] + cin;
	assign overflow = cout ^ lcout;
endmodule

module RingCounter(out,clear,clock);
    parameter N = 4;
    input clear,clock;
	 integer i;
    output reg [N - 1:0] out=4'b0000;
    always @ (posedge clear or posedge clock) begin
        if (clear == 1'b1) out <= 4'b0001;
        else begin
				for (i = 0; i < N - 1; i = i + 1) begin
					out[i] <= out[i+1];
				end
				out[N - 1] <= out[0];
		  end
    end
endmodule


module DivideByNImpl(clk, in, out, enable, load, clear);
	parameter N = 4;
	parameter Limit = 10;
	input clk, load, clear, enable;
	input [N - 1:0] in;
	output reg [N - 1:0] out;
	always @ (posedge clk or posedge clear) begin
		if (clear == 1'b1) begin
			out <= 'b0;
		end
		else if (load == 1'b1) begin
			out <= in;
		end
		else if (enable == 1'b1) begin
			out <= out + 1;
		end
		else begin
			out <= out;
		end
	end
endmodule

module DivideByN(clk, in, out, enable, load, clear);
	parameter N = 4;
	parameter Limit = 10;
	input [N - 1:0] in;
	input clk, clear, enable;
	output [N - 1:0] out;
	reg loadr;
	output load;

	assign load = loadr;
	
	DivideByNImpl #(N, Limit) Impl(clk, in, out, enable, load, clear);
	always @ * begin
		if (out == Limit) begin
			loadr <= 1'b1;
		end
		else begin
			loadr <= 1'b0;
		end
	end
	
endmodule

module ShiftReg (Q, Dout, Din, clock);
	parameter N = 4;
	input clock, Din;
	output Dout;
	output [N - 1:0] Q;
	reg [N - 1:0] Q;
	always @ (posedge clock) begin
		Q[N - 2:0] <= Q[N - 1:1];
		Q[N - 1] <= Din;
	end
	assign Dout = Q[0];
endmodule

module ShifterL (Q, I, in, sh);
	parameter size = 4;
	input in, sh;
	input [size-1:0] I;
	output [size-1:0] Q;
	reg [size-1:0] Q;
	always @ (sh, in, I) begin
		if (sh) begin 
			Q[size-1:1] = I[size-2:0];
			Q[0] = in;
		end
		else Q = I;
	end
endmodule

module ShifterR (Q, I, in, sh);
	parameter size = 4;
	input in, sh;
	input [size-1:0] I;
	output [size-1:0] Q;
	reg [size-1:0] Q;
	always @ (sh, in, I) begin
		if (sh) begin 
			Q[size-2:0] = I[size-1:1];
			Q[size-1] = in;
		end
		else Q = I;
	end
endmodule

module SPGBlock(a, b, cin, P, G, s);
	input a, b, cin;
	output P, G, s;

	assign P = a ^ b;
	assign G = a & b;
	assign s = P ^ cin;
endmodule

module CarryLookaheadAdder(a, b, cin, s, cout);
	parameter N = 4;
	input [N - 1:0] a, b;
	input cin;
	output [N - 1:0] s;
	output cout;
	genvar i;
	wire [N:0] ctemp;
	wire [N - 1:0] P;
	wire [N - 1:0] G;
	wire Pout, Gout;
	generate
		assign ctemp[0] = cin;
		assign cout = ctemp[N];
        for (i = 0; i < N; i = i + 1) begin : generate_block_cladder // to satisfy ISE
            SPGBlock(a[i], b[i], ctemp[i], P[i], G[i], s[i]);
			assign ctemp[i + 1] = G[i] | (P[i] & ctemp[i]);
        end
    endgenerate
endmodule

module ComparatorStage(a, b, igt, ieq, ilt, ogt, oeq, olt);
	input a, b, igt, ieq, ilt;
	output ogt, oeq, olt;

	assign ogt = igt | (ieq & a & ~b);
	assign olt = igt | (ieq & ~a & b);
	assign oeq = ieq & ~(a ^ b);
endmodule