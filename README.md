# Corporate-Scandal

企業の不祥事ニュースと、その直後の株価の動きの法則性を分析する。

# ニュースソース

- [Google News](https://news.google.com/)

日本の場合、1990年頃から最新までのネット記事が載っている。
日付の範囲指定（before/after:yyyy-mm-dd）も可能で、「不正　after:1990-1-1　before:1999-1-1」という入力のURLは、次のようになる。1回の検索で最大80件？（要確認）の記事を取得可能。
 https://news.google.com/search?q=%E4%B8%8D%E6%AD%A3%E3%80%80after%3A1990-1-1%E3%80%80before%3A1999-1-1&hl=ja&gl=JP&ceid=JP%3Aja


 TODO
 - 最大件数80?に達したら、分割して80以下にする必要がある。全ての記事を抽出するために。