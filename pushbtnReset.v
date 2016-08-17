module pushbtnReset (
	clk,
	rstIn,
	rstOut
);

input clk;
input rstIn;
output rstOut;
wire rstOut;

reg temp0 = 1'b0;
//reg temp1 = 1'b0;
reg rst_sync = 1'b0;

assign rstOut = rst_sync;
/*
always @(negedge rstIn) begin
	temp1 <= 1'b1;
	end
*/
always @(posedge clk) begin
	if(!rstIn) begin
		temp0 <= 1'b1;
		rst_sync <= 1'b1;
	end else if(temp0 & rstIn) begin
		temp0 <= 1'b0;
//		temp1 <= 1'b0;
		rst_sync <= 1'b0;
	end
end

endmodule
