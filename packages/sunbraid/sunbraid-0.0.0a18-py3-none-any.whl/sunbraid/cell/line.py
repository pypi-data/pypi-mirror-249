import uuid
import seaborn as sns
import numpy as np

DASH_ORDER = []
def get_colors(palette, N):
    return [f'rgb{tuple(c)}' for c in (np.array(sns.color_palette(palette, N))*255).astype(int)]


def prep_group(df, x, y, color, line_dash):
    result = df.sort_values(x).copy()
    return (
        result
        .assign(x = lambda d: d[x])
        .assign(y = lambda d: d[x])
    )

def prep(df, row, x, y, color, line_dash):
    (
        df.groupby(row)
    )



def make_lineplot(data, height=50):
    random_id = str(uuid.uuid4()).replace('-', '')
    return f"""
    <div class="magnifiable">
        <div id="rdivRUID{random_id}"></div>
    </div>
    <script>
        const dataRUID{random_id} = {data};
        createLinePlot(dataRUID{random_id},  'rdivRUID{random_id}', {height});
    </script>
"""