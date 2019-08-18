# KomatsuBlokus
## プロジェクトの概要
これは早稲田大学小松幸夫研究室の「建築のジョー」がBlokusが好きすぎてPC上で開発しようと考え、  
研究室の仲間と共にゲームシステムとAIの開発を目指すプロジェクトです！

## 開発メンバー
- 高砂（建築のジョー）、山本、村松、神田、山田

## 開発環境
- Python3
- pygame

## Blokusとは
- 4色のブロックを盤面に広げていくボードゲーム
- ルールは単純でブロック同士が頂点で接するように置いていくだけ
- 他のピースをすり抜けて相手の陣地に侵入したり、相手のピースを置けないように妨害するなど様々な戦略がある
- 詳しくは[この記事](https://boku-boardgame.net/blokus)にて

## 動作例
![a011c2e8c2d8cb76cfb502a0718df35d](https://user-images.githubusercontent.com/38747501/63224265-ab37f000-c1fc-11e9-8a71-88dbcb187185.gif)

## ブロック一覧表
- 全21種のブロックとそれに対応するアルファベット（黒マスは回転軸）
- ルール引用元：[ブロックスデュオ プログラム対戦 要領](http://hp.vector.co.jp/authors/VA003988/gpcc/07g1.htm)
- 画像引用元：[古川 晋也（2014）C 言語による BlokusDuo 対戦プログラムの作成](http://www.hpc.se.ritsumei.ac.jp/papers/b14/furukawa.pdf)
![ブロック一覧表](https://github.com/JoeTakasuna/KomatsuBlokus/blob/master/%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E4%B8%80%E8%A6%A7%E8%A1%A8.png)

## 命名規則
| 対象 | ルール | 例 |
|:---:|:-----:|:--:|
| ファイル | 最初大文字 + 大文字区切り | BlockTable.py |
| クラス | 最初大文字 + 大文字区切り | BlockTable |
| メソッド | 全小文字 + アンダースコア区切り | make_board |
| 関数 | 全小文字 + アンダースコア区切り | change_turn |
| 変数 | 全小文字 + アンダースコア区切り | current_player |
| 定数 | 全大文字 + アンダースコア区切り | TILE_NUMBER |

## 簡単で網羅的なテスト方法
1. TILE_NUMBERを5、プレイヤー数を2、CP数を0にする
2. 緑：e0
3. 黄：j0
4. 緑：e0(check_input：使用済みかどうかのチェック)
5. 緑：j0(settable_area_exist_check：置ける場所があるかのチェック)
6. 緑：a0→zでキャンセル(cancel_selected：キャンセル)
7. 緑：a0
8. 黄：自動パス（any_block_settable_check：置けるブロックがあるかのチェック）
9. 緑：自動パス（score_check:スコア計算）
