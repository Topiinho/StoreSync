if object_id ('sp_Cadastro_Fornecedor', 'p') is not NULL
	drop procedure sp_Cadastro_Fornecedor;
go


CREATE PROCEDURE sp_Cadastro_Fornecedor
	@Nome nvarchar(100),
	@Descricao nvarchar(max)
AS
BEGIN
	if exists (
		select 1
		from tbFornecedor
		where NomeFornecedor = @Nome
	)
	begin
		update tbFornecedor
			set dsFornecedor = @Descricao
			where NomeFornecedor = @Nome
			return;
	end

	insert into tbFornecedor (NomeFornecedor, dsFornecedor)
		values (@Nome, @Descricao)

END
GO
