<template>
  <v-container>
    <v-treeview :items="items"></v-treeview>
  </v-container>
</template>

<script>
export default {
  name: "Planet",
  data: function () {
    return {
      items: [
        {
          id: 1,
          name: "太陽系",
          children: [
            { id: 2, name: "水星" },
            { id: 3, name: "金星" },
            { id: 4, name: "地球", children: [{ name: "月" }] },
            {
              id: 5,
              name: "火星",
              children: [{ name: "フォボス" }, { name: "ダイモス" }],
            },
            {
              id: 6,
              name: "木星",
              children: [
                { name: "イオ" },
                { name: "エウロパ" },
                { name: "ガニメデ" },
                { name: "カリスト" },
              ],
            },
            {
              id: 7,
              name: "土星",
              children: [{ name: "たくさん（82個）" }],
            },
            {
              id: 8,
              name: "天王星",
              children: [{ name: "アリエル" }],
            },
            {
              id: 9,
              name: "海王星",
              children: [{ name: "トリトン" }],
            },
          ],
        },
      ],
    };
  },
};
</script>