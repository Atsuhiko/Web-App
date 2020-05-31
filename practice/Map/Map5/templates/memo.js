
const addMemo = () => {

    // JSでimgタグのオブジェクトを作成
    const p = document.createElement('p');
    const addMemoPlace = document.getElementById('addMemoPlace').value;
    p.innerHTML = `- ${addMemoPlace}が登録されました！`;

    // articleタグの子要素としてimgを追加
    const article = document.querySelector('article');
    article.appendChild(p);
}

// ボタンをクリックしたことをトリガーに処理を走らす
const addMemoBtn = document.querySelector('.addMemoBtn');
addMemoBtn.onclick = () => {
    return addMemo();
};
