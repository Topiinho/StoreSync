try:
    from PIL import Image
    print("PIL importado com sucesso!")
except ImportError as e:
    print(f"Erro ao importar PIL: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}") 