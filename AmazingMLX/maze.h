#ifndef MAZE_H
#define MAZE_H

#include "mlx.h"
#include <stdlib.h>
#include <unistd.h>

#define WIDTH 800
#define HEIGHT 600

typedef struct s_data
{
    void    *mlx;
    void    *win;
    void    *img;
    char    *addr;
    int     bpp;
    int     line_len;
    int     endian;

    int     x;
    int     y;
}   t_data;

void    put_pixel(t_data *data, int x, int y, int color);
void    draw_something(t_data *data);
int     key_hook(int keycode, void *param);
int     close_window(void *param);
void	draw_circle(t_data *data, int cx, int cy, int r, int color);
void    render(t_data *data);

#endif
