if object_id ('sp_Cadastro_Tag', 'p') is not NULL
	drop procedure sp_Cadastro_Tag;
go


CREATE PROCEDURE sp_Cadastro_Tag
	@Tag nvarchar(max)
AS
BEGIN
	if exists (
		select 1
		from tbTags
		where Tag = @Tag
	)
	begin
		print 'Essa tag já existe!'
		return;
	end

	insert into tbTags (Tag)
		values (@Tag)

END
GO
