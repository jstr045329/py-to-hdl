library IEEE;
use IEEE.std_logic_1164.all;

entity dff is 
        generic(width : integer);
        port(
              clk   :   in    std_ulogic_vector(0 downto 0);
              rst   :   in    std_ulogic_vector(0 downto 0);
              d     :   in    std_ulogic_vector(width-1 downto 0);
              q     :   out   std_ulogic_vector(width-1 downto 0));
end dff;

architecture dff_arch of dff is
        signal q0 : std_ulogic_vector(width-1 downto 0) := (others => '0');
begin

process(clk)
begin
        if rising_edge(clk) then
                q0 <= d;
        end if;
end process;

q <= q0;

end dff_arch;
