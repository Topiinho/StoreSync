
if OBJECT_ID ('sp_Compra', 'p') is not NULL
	drop procedure sp_Compra;
go


CREATE PROCEDURE sp_Compra
	@idFornecedor int,
	@idProduto int,
	@Quantidade smallint,
	@CustoTotal decimal(9,2),
	@Data smalldatetime

AS
BEGIN
	
	-- Verifica se existe o fornecedor fornecido
	if not exists (
		select 1
		from tbFornecedor
		where idFornecedor = @idFornecedor
	)
	Begin
		print 'Esse codigo de fornecedor não existe'
		return;
	end

	-- Verifica se existe o produto fornecido
	if not exists (
		select 1
		from tbProduto
		where idProduto = @idProduto
	)
	Begin
		print 'Esse codigo de produto não existe'
		return;
	end

	-- Declara a variavel @CustoUnitario e já define que ela é igual a divisão de @CustoTotal por @Quantidade
	declare @CustoUnitario decimal(9,2)
	set @CustoUnitario = @CustoTotal / @Quantidade

	-- Insere umaa nova linha na tabela compra com os dados fornecidos
	insert into tbCompra(idProduto, idFornecedor, CustoUnitario, Quantidade, CustoTotal, Data)
		values (@idProduto, @idFornecedor, @CustoUnitario, @Quantidade, @CustoTotal, @Data);


	declare @Estoque smallint
	declare @CustoMedio decimal(9,2)

	select  @Estoque = Estoque,
			@CustoMedio = CustoMedio
		from tbProduto 
		where idProduto = @idProduto

	set @Estoque = @Estoque + @Quantidade
	set @CustoMedio = (@CustoTotal + (@CustoMedio * @Estoque)) / @Estoque

	update tbProduto
		set Estoque = @Estoque,
			CustoMedio = @CustoMedio
		where idProduto = @idProduto


END
GO
