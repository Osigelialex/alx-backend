import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
const app = express();
const getAsync = promisify(client.get).bind(client);

const listProducts = [
  { Id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { Id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { Id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { Id: 4, name: "Suitcase 1050", price: 550, stock: 5 }
];

const getItemById = (id) => {
  const item = listProducts.filter((product) => product.Id === id);
  return item;
};

const reserveStockById = (itemID, stock) => {
  client.set(itemID.toString(), stock.toString());
};

const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(itemId.toString());
  if (stock !== null) {
    return stock;
  }

  const item = getItemById(itemId);
  if (item.length === 0) {
    return JSON.stringify({ "status": "Product not found" });
  } else {
    return JSON.stringify({ item: item });
  }
};

app.get('/list_products', (req, res) => {
  res.send(JSON.stringify(listProducts));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const result = await getCurrentReservedStockById(itemId);
  res.send(result);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const result = await getCurrentReservedStockById(itemId);
  if (JSON.parse(result).status === 'Product not found') {
    res.send(result);
    return;
  }

  const itemStock = JSON.parse(result).item[0].stock;
  if (itemStock > 0) {
    reserveStockById(itemId, itemStock - 1);
    res.send(JSON.stringify({ "status": "Reservation confirmed", "itemId": itemId}));
  } else {
    res.send(JSON.stringify({ "status": "Not enough stock available", "itemId": itemId}));
  }
});

app.listen(1245, () => {
  console.log('Server is running on port 1245');
});
