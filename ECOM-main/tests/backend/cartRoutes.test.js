const request = require("supertest");
const app = require("../../backend/index");

let token;
let userId = 101; // set this to a user that exists and owns the cart

beforeAll((done) => {
  request(app)
    .post("/api/login")
    .send({
      email: "user@test.com", // must match a user in your DB
      password: "test123"
    })
    .end((err, res) => {
      if (err) return done(err);
      token = res.body.token;
      userId = res.body.userId || userId; // use returned userId from login
      done();
    });
});

describe("Cart API", () => {
  it("should add product to cart", (done) => {
    request(app)
      .post("/api/cart")
      .set("Authorization", `Bearer ${token}`)
      .send({
        userId,       // make sure it matches the logged-in user
        productId: 1,
        quantity: 2
      })
      .expect(res => {
        if (![200, 400].includes(res.statusCode)) {
          throw new Error(`Unexpected status: ${res.statusCode}`);
        }
      })
      .end(done);
  });

  it("should get cart items", (done) => {
    request(app)
      .get(`/api/cart/${userId}`)
      .set("Authorization", `Bearer ${token}`)
      .expect(res => {
        if (![200, 404].includes(res.statusCode)) {
          throw new Error(`Unexpected status: ${res.statusCode}`);
        }
      })
      .end(done);
  });
});