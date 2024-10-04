if object_id ('sp_Cadastro_Produto', 'p') is not NULL
	drop procedure sp_Cadastro_Produto
go


CREATE PROCEDURE sp_Cadastro_Produto
	@Nome nvarchar(100),
	@Modelo nvarchar(MAX),
	@Tags nvarchar(MAX),
	@Descricao nvarchar(MAX)
AS
BEGIN
	if exists (
		select 1
		from tbProduto
		where NomeProduto = @Nome
			and Modelo = @Modelo
	)
	begin
		update tbProduto
			set Descricao = @Descricao
			where NomeProduto = @Nome
				and Modelo = @Modelo
		return;
	end
	
	insert into tbProduto (NomeProduto, Modelo, Tags, CustoMedio, Estoque, Descricao)
		values (@Nome, @Modelo, @Tags, 0, 0, @Descricao)

END
GO
