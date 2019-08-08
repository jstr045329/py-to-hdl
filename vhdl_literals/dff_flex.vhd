library IEEE;
use IEEE.std_logic_1164.all;

entity dff is 
        generic(w : integer);
        port(
              clk       : in    std_ulogic_vector(0 downto 0);
              rst_0     : in    std_ulogic_vector(0 downto 0) := (others => '0');
              rst_1     : in    std_ulogic_vector(0 downto 0) := (others => '0');
              rst_2     : in    std_ulogic_vector(0 downto 0) := (others => '0');
              rst_3     : in    std_ulogic_vector(0 downto 0) := (others => '0');
              rst_val_0 : in    std_ulogic_vector(width-1 downto 0) := (others => '0');
              rst_val_1 : in    std_ulogic_vector(width-1 downto 0) := (others => '0');
              rst_val_2 : in    std_ulogic_vector(width-1 downto 0) := (others => '0');
              rst_val_3 : in    std_ulogic_vector(width-1 downto 0) := (others => '0');
              en        : in    std_ulogic_vector(0 downto 0) := (others => '1');
              d         : in    std_ulogic_vector(width-1 downto 0) := (others => '0');
              t         : in    std_ulogic_vector(width-1 downto 0) := (others => '0');
              q         : out   std_ulogic_vector(width-1 downto 0));
end dff;

architecture dff_arch of dff is
        signal q0 : std_ulogic_vector(width-1 downto 0) := (others => '0');
begin

process(clk)
begin
        if rising_edge(clk) then
                if rst_0 = '1' then 
                        q0 <= rst_val_0;
                elsif rst_1 = '1' then
                        q0 <= rst_val_1;
                else
                        if en = '1' then
                                if rst_2 = '1' then
                                        q0 <= rst_val_2;
                                elsif rst_3 = '1' then
                                        q0 <= rst_val3;
                                elsif t = '1' then
                                        q0 <= not q0;
                                else
                                        q0 <= d;
                                end if;
                        end if;
                end if;
        end if;
end process;

q <= q0;

end dff_arch;



