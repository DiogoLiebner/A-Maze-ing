#ifndef MAZE_H
#define MAZE_H

#include "mlx.h"
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

#define WIDTH 800
#define HEIGHT 600
#define CELL_SIZE 20

typedef struct s_cell
{
    int     walls;
}   t_cell;

typedef struct s_point
{
    int     x;
    int     y;
} t_point;

typedef struct s_data
{
    void    *mlx;
    void    *win;
    void    *img;
    char    *addr;
    int     bpp;
    int     line_len;
    int     endian;

    int     win_w;
    int     win_h;
    
    int     x;
    int     y;

    t_cell  **grid;
    int     rows;
    int     cols;

    int     entry_x;
    int     entry_y;

    int     exit_x;
    int     exit_y;

    char    *path;

    t_point *path_cells;
    int     path_len;
    int     path_mode;
}   t_data;




void    put_pixel(t_data *data, int x, int y, int color);
void    draw_something(t_data *data);
int     key_hook(int keycode, void *param);
int     close_window(void *param);
void	draw_circle(t_data *data, int cx, int cy, int r, int color);
void    render(t_data *data);
void    render_maze(t_data *data);
void    draw_line(t_data *data, int x1, int y1, int x2, int y2);
void    parse_maze_file(t_data *data, char *filename);
void    allocate_grid(t_data *data, int rows, int cols);
static int  count_cols(char **split);
static int  count_rows(char *filename);
char	**ft_split(char const *s, char c);
void build_path_cells(t_data *d);
int is_on_path(t_data *d, int x, int y);
void fill_cell(t_data *d, int x, int y, int w, int h, int color);
void draw_path_line(t_data *d);

#endif

