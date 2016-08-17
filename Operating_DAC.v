

module Operating_DAC
(
	trigger,
	reset,
	dacVal
);

parameter PRECISION = 12;

input trigger;
input reset;
output [PRECISION-1:0] dacVal;
reg [PRECISION-1:0] dacVal = {PRECISION {1'b0}};

reg [PRECISION-1:0] maxVal = {PRECISION {1'b1}};

always @(posedge trigger, posedge reset) begin
	if (reset == 1'b1) begin
		dacVal <= {PRECISION {1'b0}};
	end else if (trigger == 1'b1) begin
		if (dacVal == maxVal) begin
			dacVal <= {PRECISION {1'b0}};
		end else begin
			dacVal <= dacVal + 1'b1;
		end
	end
end

endmodule
