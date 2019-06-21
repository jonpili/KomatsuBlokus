#include <algorithm>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>
#include <assert.h>
#include "board.h"
#include "search.h"
#include "opening.h"
#include "str.h"
using namespace std;

class Player {
public:
    virtual Move get_move(Board* b, const Move* history) = 0; 
};

class Com_30min : public Player {
public:
    Com_30min() : time_(1800.0) {}
    virtual Move get_move(Board* b, const Move* history);
protected:
    SearchResult search(Board* b);
private:
    double time_;
};

SearchResult Com_30min::search(Board* b)
{
    int max_depth, stop_sec, timeout_sec;

    int stage = (b->turn() + 1) / 2;

    if (stage < 7) {
	int t = 7 - stage;
	timeout_sec = (int)min((time_ - 960) / t * 1.5, time_-960);
	stop_sec = timeout_sec / (stage < 4 ? 20 : 12);
	max_depth = 7;
    }
    else if (stage < 10) {
	int t = 9 - stage;
	timeout_sec = (int)(time_ - 240 - 240*t);
	stop_sec = timeout_sec / 4;
	max_depth = 12;
    }
    else if (stage < 13) {
	int t = 12 - stage;
	try { return wld(b, 10); } catch (Timeout& e) {}
	time_ -= 10;
	timeout_sec = (int)(time_ - 60 - 60*t);
	stop_sec = timeout_sec / 2;
	max_depth = 15;
    }
    else if (stage < 14)
	return wld(b, 1800);
    else
	return perfect(b);

    printf("stop: %d  timeout: %d  time: %.3f\n",
	   stop_sec, timeout_sec, time_);

    return search_negascout(b, max_depth, stop_sec, timeout_sec);
}

Move Com_30min::get_move(Board* b, const Move* history)
{
    Move move;
    int score = 100;
    clock_t turn_start = clock();
    visited_nodes = 0;

    move = opening_move(b, history);
    if (move == INVALID_MOVE) {
	SearchResult result = search(b);
	move = result.first;
	score = result.second;
    }
    assert(b->is_valid_move(move));

    double sec = (double)(clock() - turn_start) / CLOCKS_PER_SEC;
    time_ -= sec;

    printf("%s (%d)\n", move.fourcc().c_str(), score);
    printf(" %d nodes / %.3f sec (%d nps) %.3f sec remaining\n\n",
	   visited_nodes, sec, (int)(visited_nodes / sec), time_);
    printf("%s@%d: %s\n",
	   b->is_violet() ? "violet" : "orange", b->turn() + 1,
	   move.fourcc().c_str());

    return move;
}

class Com_5sec : public Player {
public:
    virtual Move get_move(Board* b, const Move* history);
};

Move Com_5sec::get_move(Board* b, const Move* history)
{
    Move move;
    int score = 100;
    clock_t turn_start = clock();
    visited_nodes = 0;

    move = opening_move(b, history);
    if (move == INVALID_MOVE) {
	SearchResult r;
	if (b->turn() < 25)
	    r = search_negascout(b, 10, 2, 5);
	else if (b->turn() < 27)
	    r = wld(b, 1000);
	else
	    r = perfect(b);
	move = r.first;
	score = r.second;
    }
    assert(b->is_valid_move(move));

    double sec = (double)(clock() - turn_start) / CLOCKS_PER_SEC;

    printf("%s (%d)\n", move.fourcc().c_str(), score);
    printf(" %d nodes / %.3f sec (%d nps)\n\n",
	   visited_nodes, sec, (int)(visited_nodes / sec));
    printf("%s@%d: %s\n",
	   b->is_violet() ? "violet" : "orange", b->turn() + 1,
	   move.fourcc().c_str());

    return move;
}

class Human : public Player {
public:
    virtual Move get_move(Board* b, const Move* history);
};

Move Human::get_move(Board* b, const Move*)
{
    char buf[100];
    Move m;
    printf("\n");
    for (;;) {
	printf("%s@%d> ", b->is_violet() ? "violet" : "orange", b->turn() + 1);
	fflush(stdout);
	if (fgets(buf, sizeof buf, stdin) == NULL)
	    exit(1);

	if (strncmp(buf, "----", 4) == 0)
	    return PASS;

	int x, y, d;
	char c;
	if (sscanf(buf, "%1X%1X%c%1d", &x, &y, &c, &d) == 4 &&
	    x >= 1 && x <= 14 && y >= 1 && y <= 14 &&
	    tolower(c) >= 'a' && tolower(c) <= 'u' &&
	    d >= 0 && d <= 7)
	{
	    m = Move(buf);
	    if (b->is_valid_move(m))
		return m;
	}
    }
}

void game(Player* violet, Player* orange)
{
    Board b;
    Move history[44];

    for (int npass = 0; npass < 2;) {
	b.show();
	fflush(stdout);

	Move m = (b.is_violet() ? violet : orange)->get_move(&b, history);
	history[b.turn()] = m;

	b.do_move(m);

	npass = m.is_pass() ? npass+1 : 0;
    }
    printf("\nresult: violet (%d) - orange (%d)\n",
	   b.violet_score(), b.orange_score());
}

int select_color()
{
    char buf[80];
    int color;

    do {
	printf(STR_COLOR_SELECT);
	fflush(stdout);
	if (fgets(buf, sizeof buf, stdin) == NULL)
	    exit(1);
	color = atoi(buf);
    } while (color < 1 || color > 4);

    return color;
}

int main(int argc, char *argv[])
{
    srand(time(NULL));

    int color = 0;
    bool contest = false;
    for (int i = 1; i < argc; i++) {
	if (argv[i][0] == '-' && argv[i][1] >= '1' && argv[i][1] <= '4')
	    color = argv[i][1] - '0';
	else if (strcmp(argv[i], "-c") == 0)
	    contest = true;
    }
    if (color == 0)
	color = select_color();

    Player* violet = (color & 1) ? (Player*)new Human() :
	contest ? (Player*)new Com_30min() : (Player*)new Com_5sec();
    Player* orange = (color & 2) ? (Player*)new Human() : 
	contest ? (Player*)new Com_30min() : (Player*)new Com_5sec();
    game(violet, orange);
    delete violet;
    delete orange;

    return 0;
}
