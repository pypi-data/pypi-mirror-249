module tb_mpegChannel;

reg clk;
reg rst;

initial begin
    $from_myhdl(
        clk,
        rst
    );
end

mpegChannel dut(
    clk,
    rst
);

endmodule
