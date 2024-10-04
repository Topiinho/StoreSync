
if object_id ('sp_Venda', 'p') is not NULL
	drop procedure sp_Venda;
go


CREATE PROCEDURE sp_Venda
	@idProduto int,
	@Quantidade smallint,
	@ValorVenda decimal(9,2),
	@Data smalldatetime
AS
BEGIN
	
	if not exists (
		select 1
		from tbProduto
		where idProduto = @idProduto
	)
	begin
		print 'Esse produto não está cadastrado'
	end


	if exists (
		select 1
		from tbProduto
		where idProduto = @idProduto
			and Estoque >= @Quantidade
	)
	begin
		declare @ValorCusto decimal(9,2)
		
		select @ValorCusto = CustoMedio * @Quantidade
			from tbProduto
			where idProduto = @idProduto

		update  tbProduto
			set Estoque = Estoque - @Quantidade
			where idProduto = @idProduto

		declare @ValorLucro decimal(9,2)
		set @ValorLucro = @ValorVenda - @ValorCusto

		insert into tbVendaProduto (idProduto, Quantidade, ValorCusto, ValorVenda, ValorLucro,Data)
			values (@idProduto, @Quantidade, @ValorCusto, @ValorVenda, @ValorLucro,@Data)

	end
	else
	begin
		print 'Não tem estoque disponivel desse produto'
		return;
	end

END
GO
