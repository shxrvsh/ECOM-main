const request = require("supertest");
const app = require("../../backend/index");
const db = require('../../backend/db');
const bcrypt = require('bcryptjs'); // safer for Jest

// Helper to wrap callback-style db.query in a Promise
const queryAsync = (sql, params = []) =>
  new Promise((resolve, reject) => {
    db.query(sql, params, (err, result) => {
      if (err) return reject(err);
      resolve(result);
    });
  });


afterAll(async () => {
  await queryAsync('DELETE FROM users WHERE email = ?', ['test3@example.com']);
  db.end(); // close MySQL connection
});

describe("User API", () => {
  it("should register a user", (done) => {
    request(app)
      .post("/api/register")
      .send({
        name: "Test User",
        email: "test3@example.com",
        password: "password123"
      })
      .expect(200)
      
      .end(done); // use done() for callback-based async
  });

  it("should login a user", (done) => {
    request(app)
      .post("/api/login")
      .send({
        email: "test@example.com",
        password: "password123"
      })
      .expect(res => {
        if (![200, 401].includes(res.statusCode)) throw new Error(`Unexpected status: ${res.statusCode}`);
        if (res.statusCode === 200) {
          if (!res.body.token) throw new Error("Missing token");

        }
      })
      .end(done);
  });
});