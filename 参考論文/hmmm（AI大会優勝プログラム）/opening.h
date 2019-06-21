#ifndef OPENING_H_
#define OPENING_H_

extern const unsigned short violet_first_moves[];
extern const unsigned short orange_first_moves[];

Move opening_move(Board* b, const Move* history);

#endif // OPENING_H_
