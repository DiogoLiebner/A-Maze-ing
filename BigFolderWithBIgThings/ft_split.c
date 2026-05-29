/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafmonte <rafmonte@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 13:28:06 by rafmonte          #+#    #+#             */
/*   Updated: 2026/05/26 15:17:23 by rafmonte         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include <string.h>

void	ft_initiate_vars(size_t *x, int *y, int *z)
{
	*x = 0;
	*y = 0;
	*z = -1;
}

int	word_count(char const *c, char limit)
{
	int	i;
	int	count;
	int	will_count;

	i = 0;
	count = 0;
	will_count = 1;
	while (c[i])
	{
		if (c[i] != limit && will_count == 1)
		{
			will_count = 0;
			count++;
		}
		else if (c[i] == limit)
			will_count = 1;
		i++;
	}
	return (count);
}

char	*fill_word(char const *c, int start, int end)
{
	int		i;
	int		j;
	int		count;
	char	*str;

	if (!c || start < 0 || end < 0 || end < start)
		return (NULL);
	j = 0;
	count = end - start;
	i = start;
	str = malloc(count + 1);
	if (!str)
		return (NULL);
	i = start;
	while (i < end)
		str[j++] = c[i++];
	str[j] = '\0';
	return (str);
}

void	*ft_free_2(char **c, int final_position)
{
	int	i;

	i = 0;
	while (i <= final_position)
	{
		free(c[i]);
		i++;
	}
	free(c);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	size_t		i;
	int			j;
	int			beninging;
	char		**str_array;

	ft_initiate_vars(&i, &j, &beninging);
	str_array = malloc((word_count(s, c) + 1) * sizeof(char *));
	if (!str_array)
		return (NULL);
	while (i <= strlen(s) && s[i] != '0')
	{
		if (s[i] != c && beninging < 0)
			beninging = i;
		else if ((s[i] == c || i == strlen(s)) && beninging >= 0)
		{
			str_array[j] = fill_word(s, beninging, i);
			if (!str_array[j])
				return (ft_free_2(str_array, j));
			j++;
			beninging = -1;
		}
		i++;
	}
	str_array[j] = NULL;
	return (str_array);
}
