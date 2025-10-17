# 最簡可計算範例：p-adic Teichmüller, Anabelian Geometry, Arakelov/Hodge, Frobenioid

這份筆記整理了四個數論與幾何高階理論（出現在 IUT 理論中）的最簡且可計算的實例範例，包含 p-adic Teichmüller 理論、Anabelian Geometry、Arakelov/Hodge 技巧與 Mochizuki 自創之 Frobenioid 等構造。每節包含直觀說明與可操作的簡單範例。

## 1. p-adic Teichmüller — 最簡可算範例：Tate 曲線（Tate uniformization）

### 重點
- 對 p-adic 場（如 \\(\\mathbb{Q}_p\\)）上的橢圓曲線，Tate 曲線 \\(E_q\\) 是由 q-展開式定義的，當 \\(|q|_p < 1\\)。
- 它提供了 p-adic 上的 Teichmüller uniformization，並且可以用級數截斷來做數值計算。

### 可操作步驟
1. 取 p = 5。
2. 設定 q = 1/125 ≈ 5^(-3)。
3. 利用 Tate 曲線公式展開 Weierstrass 係數 \\(a_4(q)\\), \\(a_6(q)\\)。
4. 建立曲線 \\(y^2 = x^3 + a_4x + a_6\\)，計算點與加法。

👉 可用 Sage 或 Python 編寫程式做數值計算。

---

## 2. Anabelian Geometry — 最簡可算範例：\\(\\mathbb{P}^1 \\setminus \\{0,1,\\infty\\}\\) 的 monodromy/Belyi

### 重點
- Grothendieck anabelian 幾何主張某些「hyperbolic」曲線可以從其 étale 基本群（含 Galois 作用）中完全重建。
- 透過 Belyi map（有理函數只在 0,1,∞ 處分歧）可對應到有限覆蓋與置換群資料。

### 可操作步驟
1. 選一個簡單 Belyi map，如 \\(f(z) = z^2\\)。
2. 計算其 ramification 資料：在 0,1,∞ 的分支情況。
3. 更進階例子：列舉 degree 3~4 的 permutation triple (monodromy)，例如 \\((\\sigma_0,\\sigma_1,\\sigma_\\infty)\\)，滿足 \\(\\sigma_0 \\sigma_1 \\sigma_\\infty = 1\\)。

👉 可用 GAP/Sage 探索 monodromy group，產生 dessins d’enfants。

---

## 3. Arakelov/Hodge 技巧 — 最簡可算範例：有理點的 height 計算

### 重點
- Arakelov 理論將阿基米德與非阿基米德的幾何合併，產生對數的 global height。
- 對 \\(\\mathbb{Q}\\) 上的點 \\(x = \\frac{a}{b}\\)，naive height \\(h(x) = \\log \\max(|a|, |b|)\\)。

### 可操作步驟
- \\(x = \\frac{3}{2}\\) → \\(h(x) = \\log(3) ≈ 1.0986\\)
- 更一般地：向量 \\([a_0:...:a_n]\\) → height = \\(\\log \\max |a_i|\\)

👉 可用 Python 實作：取整數比，計算 log-max。

---

## 4. Frobenioid（Mochizuki 構造）— 最簡可算範例：monoid 的 Frobenioid

### 重點
- Frobenioid 是將 divisor/line bundle 資料抽象為 category，Mochizuki 用以操控高度。
- 最簡例子：令 monoid \\(M = \\mathbb{N}\\)，物件為整數，態射為乘法（如 \\(m → m+n\\)）。

### 可操作步驟（toy 模型）
1. 物件：\\(1, p, p^2, \\dots\\)
2. 態射：乘以 \\(p^k\\)，合成為 \\(p^k \\cdot p^l = p^{k+l}\\)
3. 設 degree 函數 \\(\\deg(p^n) = n\\)，定義新尺度 \\(T(n) = n + \\lfloor n/2 \\rfloor\\)，比較 degree 差異。

👉 可用 Python 列出物件、態射與兩種尺度下的度差比較表。

---

## 延伸資源
- [Mochizuki, Overview of IUT](https://www.kurims.kyoto-u.ac.jp/~motizuki/papers-english.html)
- [Yamashita, ABC proof overview (2022)](https://arxiv.org/abs/2203.13332)
- [Deninger on Arakelov](https://www.uni-muenster.de/IVV5WS/WebHop/user/deninger/publ.html)
- [Belyi/Dessin notes from Lando-Zvonkin](http://www.ams.org/bookstore-getitem/item=mbk-199)