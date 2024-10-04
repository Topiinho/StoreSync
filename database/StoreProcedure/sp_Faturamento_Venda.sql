
if object_id ('sp_Faturamento_Venda', 'p') is not NULL
	drop procedure sp_Faturamento_Venda;
go

CREATE PROCEDURE sp_Faturamento_Venda
	@Data date
AS
BEGIN

	if exists (
		select 1
			from tbFaturamentoVenda
			where Data = @Data
	)
	Begin
		print 'Já foi feito o faturamento dessa data!'
		return;
	end

	if not exists (
		select 1
			from tbVendaProduto
			where Data = @Data
	)
	Begin
		print 'Não foi feito nenhuma venda nesse dia!'
		return;
	end

	declare @ValorCusto decimal(9,2)
	declare @ValorVenda decimal(9,2)
	declare @ValorLucro decimal(9,2)

	select  @ValorCusto = sum(ValorCusto),
			@ValorVenda = sum(ValorVenda),
			@ValorLucro = sum(ValorLucro)
	from tbVendaProduto
	where Data = @Data

	insert into tbFaturamentoVenda (ValorCusto, ValorVenda, ValorLucro, Data)
		values (@ValorCusto, @ValorVenda, @ValorLucro, @Data)
END
GO
