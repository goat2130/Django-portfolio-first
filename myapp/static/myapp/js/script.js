
const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault(); // フォームのデフォルトの送信処理をキャンセル
  const query = form.elements.query.value; // フォームの入力値を取得
  fetch(`/api/search?q=${query}`) // サーバーに検索クエリを送信
    .then(response => response.json())
    .then(data => {
      // 検索結果を表示する処理を記述
    });
});

app.get('/api/search', (req, res) => {
  const query = req.query.q; // 検索クエリを取得
  const posts = db.getPostsByKeyword(query); // キーワードにマッチする投稿を検索
  const users = db.getUsersByKeyword(query); // キーワードにマッチするユーザーを検索
  const results = { posts, users };
  res.json(results); // 検索結果をJSON形式で返す
});

