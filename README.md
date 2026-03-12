🎵 Spotify Music Viz

Visualização interativa de dados musicais do Spotify com foco em gênero e ano de lançamento.
Tecnologias
Biblioteca	Uso
Python 3.10+	Linguagem base
Pandas	Leitura do CSV e agregações
Matplotlib	Layout do painel e gráficos de barra e scatter
Seaborn	Violin plot e heatmap
O que é analisado

Dataset data/spotify_sample.csv com 205 faixas reais do Spotify, de 1968 a 2022, com os gêneros: pop · hip-hop · rock · indie-rock · dance · soul · k-pop

Cada linha do CSV representa uma música com as colunas: track_name, artist, genre, year, popularity, bpm, energy e danceability.
Visualizações

    Tracks por Ano — quantas músicas foram lançadas em cada ano
    Tracks por Gênero — volume total por gênero
    Gênero por Década — evolução da participação de cada gênero ao longo do tempo
    Popularidade por Gênero — distribuição estatística da popularidade via violin plot
    Energia vs Dançabilidade — correlação entre as duas métricas, colorido por gênero
    BPM por Gênero × Década — heatmap com o BPM médio cruzando gênero e período

Como rodar
bash

# Instalar dependências
pip install -r requirements.txt --break-system-packages

# Rodar
cd ~/códigos/sea-py
python3 main.py
```

A janela interativa abre automaticamente.

---

## Estrutura
```
spotify-data-viz/
├── main.py
    └── data/
            └── spotify_sample.csv

