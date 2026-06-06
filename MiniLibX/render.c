#include "maze.h"
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

/* =========================
   PIXEL DRAWING
   ========================= */

void put_pixel(t_data *data, int x, int y, int color)
{
    char *dst;

    if (x < 0 || y < 0 || x >= data->win_w || y >= data->win_h)
        return;

    dst = data->addr + (y * data->line_len + x * (data->bpp / 8));

    if (data->path_mode)
        color = 0xFF0000; // force red

    *(unsigned int *)dst = color;
}

/* =========================
   LINE DRAWING
   ========================= */

void draw_line(t_data *data, int x1, int y1, int x2, int y2, int color, int thickness)
{
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);
    int steps = (dx > dy) ? dx : dy;

    float x = x1;
    float y = y1;
    float x_inc = (float)(x2 - x1) / steps;
    float y_inc = (float)(y2 - y1) / steps;

    for (int i = 0; i <= steps; i++)
    {
        // draw thickness (square brush)
        for (int tx = -thickness / 2; tx <= thickness / 2; tx++)
        {
            for (int ty = -thickness / 2; ty <= thickness / 2; ty++)
            {
                put_pixel(data, (int)x + tx, (int)y + ty, color);
            }
        }

        x += x_inc;
        y += y_inc;
    }
}

/* =========================
   CELL FILL
   ========================= */

void fill_cell(t_data *d, int x, int y, int w, int h, int color)
{
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < w; j++)
        {
            put_pixel(d, x + j, y + i, color);
        }
    }
}

void render_entry_exit(t_data *d)
{
    int ex = d->entry_x * CELL_SIZE;
    int ey = d->entry_y * CELL_SIZE;
    int xx = d->exit_x * CELL_SIZE;
    int xy = d->exit_y * CELL_SIZE;

    fill_cell(d, ex, ey, CELL_SIZE, CELL_SIZE, 0x00FF00); // green = entry
    fill_cell(d, xx, xy, CELL_SIZE, CELL_SIZE, 0xFF0000); // red = exit
}

/* =========================
   MAIN RENDER
   ========================= */

void render_maze(t_data *d)
{
    int i;
    int j;
    int x;
    int y;
    int walls;

    render_entry_exit(d);

    for (i = 0; i < d->rows; i++)
    {
        for (j = 0; j < d->cols; j++)
        {
            x = j * CELL_SIZE;
            y = i * CELL_SIZE;
            walls = d->grid[i][j].walls;

            /* draw walls */
            if (walls & 1)
                draw_line(d, x, y, x + CELL_SIZE, y, d->wall_color,2);
            if (walls & 2)
                draw_line(d, x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE, d->wall_color, 2);
            if (walls & 4)
                draw_line(d, x, y + CELL_SIZE, x + CELL_SIZE, y + CELL_SIZE, d->wall_color, 2);
            if (walls & 8)
                draw_line(d, x, y, x, y + CELL_SIZE, d->wall_color, 2);
        }
    }

    draw_path_line(d);
}

void build_path_cells(t_data *d)
{
    int x = d->entry_x;
    int y = d->entry_y;
    int i = 0;

    int len = strlen(d->path);
    d->path_cells = malloc(sizeof(t_point) * (len + 1));
    if (!d->path_cells)
        return;

    d->path_len = 0;

    /* starting point */
    d->path_cells[d->path_len++] = (t_point){x, y};

    while (d->path[i])
    {
        char c = d->path[i];

        /* skip whitespace */
        if (c == '\n' || c == '\r' || c == ' ')
        {
            i++;
            continue;
        }

        /* compute next position (DO NOT APPLY YET) */
        int new_x = x;
        int new_y = y;

        if (c == 'W')
            new_x--;
        else if (c == 'E')
            new_x++;
        else if (c == 'N')
            new_y--;
        else if (c == 'S')
            new_y++;
        else
        {
            i++;
            continue;
        }

        /* reject invalid moves (instead of clamping) */
        if (new_x < 0 || new_y < 0 ||
            new_x >= d->cols || new_y >= d->rows)
        {
            i++;
            continue;
        }

        /* apply valid move */
        x = new_x;
        y = new_y;

        d->path_cells[d->path_len++] = (t_point){x, y};

        i++;
    }
}

void draw_path_line(t_data *d)
{
    d->path_mode = 1;

    for (int i = 1; i < d->path_progress; i++)
    {
        int x1 = d->path_cells[i - 1].x;
        int y1 = d->path_cells[i - 1].y;
        int x2 = d->path_cells[i].x;
        int y2 = d->path_cells[i].y;

        int dx = x2 - x1;
        int dy = y2 - y1;

        if (!((dx == 1 && dy == 0) ||
              (dx == -1 && dy == 0) ||
              (dx == 0 && dy == 1) ||
              (dx == 0 && dy == -1)))
        {
            continue;
        }

        int px1 = x1 * CELL_SIZE + CELL_SIZE / 2;
        int py1 = y1 * CELL_SIZE + CELL_SIZE / 2;
        int px2 = x2 * CELL_SIZE + CELL_SIZE / 2;
        int py2 = y2 * CELL_SIZE + CELL_SIZE / 2;

        draw_line(d, px1, py1, px2, py2, 0xFF0000, 2);
    }

    d->path_mode = 0;
}

int animate(void *param)
{
    t_data *d = (t_data *)param;

    if (d->path_progress > 0 && d->path_progress < d->path_len)
    {
        d->path_progress++;
        render(d);
        usleep(50000);
    }
    return (0);
}

/* =========================
   MAIN RENDER WRAPPER
   ========================= */

void render(t_data *data)
{
    if (data->img)
        mlx_destroy_image(data->mlx, data->img);

    data->img = mlx_new_image(data->mlx, data->win_w, data->win_h);
    data->addr = mlx_get_data_addr(
        data->img,
        &data->bpp,
        &data->line_len,
        &data->endian
    );

    render_maze(data);

    mlx_put_image_to_window(data->mlx, data->win, data->img, 0, 0);
}
