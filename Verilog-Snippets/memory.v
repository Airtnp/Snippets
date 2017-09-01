module memory (R_data, W_data, W_addr, R_addr, W_en, R_en, clock);
    parameter width = 32;
    parameter addr_width = 2;
    parameter number = 2**addr_width;
    output [width-1:0] R_data;
    input [width-1:0] W_data;
    input [addr_width-1:0] W_addr, R_addr;
    input W_en, R_en, clock;
    reg [width-1:0] R_data;
    reg [width-1:0] memory [number-1:0];
    always @(posedge clock) begin
        R_data = 'bz;
        if (W_en) memory[W_addr] = W_data;
        else if (R_en) R_data = memory[R_addr]; //R_data will be register
    end
endmodule