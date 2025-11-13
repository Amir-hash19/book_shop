CREATE TABLE "Account"(
    "id" BIGINT NOT NULL,
    "username" CHAR(255) NOT NULL,
    "first_name" CHAR(255) NOT NULL,
    "last_name" CHAR(255) NOT NULL,
    "phone_number" INTEGER NOT NULL,
    "email" CHAR(255)  NULL,
    "birthday" CHAR(255) NULL,
    "is_active" BOOLEAN NOT NULL,
    "is_staff" BOOLEAN NOT NULL,
    "about_me" TEXT  NULL,
    "date_created" CHAR(255) NOT NULL,
    "national_id" INTEGER NOT NULL,
    "gender" BOOLEAN NOT NULL
);
ALTER TABLE
    "Account" ADD PRIMARY KEY("id");
CREATE TABLE "Bootcamp"(
    "id" BIGINT NOT NULL,
    "title" CHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "status" BOOLEAN NOT NULL,
    "is_online" BOOLEAN NOT NULL,
    "capacity" CHAR(255) NOT NULL,
    "price" INTEGER NOT NULL,
    "instructor" CHAR(255) NOT NULL,
    "category" CHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "hours" DATE NOT NULL,
    "days" CHAR(255) NOT NULL,
    "slug" CHAR(255) NOT NULL
);
ALTER TABLE
    "Bootcamp" ADD PRIMARY KEY("id");
ALTER TABLE
    "Bootcamp" ADD PRIMARY KEY("instructor");
ALTER TABLE
    "Bootcamp" ADD PRIMARY KEY("category");
CREATE TABLE "BootCampCategory"(
    "id" BIGINT NOT NULL,
    "name" CHAR(255) NOT NULL,
    "slug" CHAR(255) NOT NULL,
    "description" TEXT NOT NULL
);
ALTER TABLE
    "BootCampCategory" ADD PRIMARY KEY("id");
ALTER TABLE
    "BootCampCategory" ADD PRIMARY KEY("name");
CREATE TABLE "BootcampRegistration"(
    "id" BIGINT NOT NULL,
    "volunteer" CHAR(255) NOT NULL,
    "bootcamp" CHAR(255) NOT NULL,
    "payment_type" BOOLEAN NOT NULL,
    "installment_count" INTEGER NOT NULL,
    "registered_at" DATE NOT NULL,
    "status" CHAR(255) NOT NULL,
    "reviewed_at" DATE NOT NULL,
    "reviewed_by" CHAR(255) NOT NULL,
    "comment" TEXT NOT NULL,
    "phone_number" CHAR(255) NOT NULL,
    "admin_comment" CHAR(255) NOT NULL,
    "slug" CHAR(255) NOT NULL
);
ALTER TABLE
    "BootcampRegistration" ADD PRIMARY KEY("id");
ALTER TABLE
    "BootcampRegistration" ADD PRIMARY KEY("volunteer");
ALTER TABLE
    "BootcampRegistration" ADD PRIMARY KEY("bootcamp");
ALTER TABLE
    "BootcampRegistration" ADD PRIMARY KEY("reviewed_by");
CREATE TABLE "BlogCategory"(
    "id" BIGINT NOT NULL,
    "name" CHAR(255) NOT NULL,
    "slug" CHAR(255) NOT NULL
);
ALTER TABLE
    "BlogCategory" ADD PRIMARY KEY("id");
CREATE TABLE "Blog"(
    "id" BIGINT NOT NULL,
    "title" CHAR(255) NOT NULL,
    "content" TEXT NOT NULL,
    "user" CHAR(255) NOT NULL,
    "uploaded_at" DATE NOT NULL,
    "slug" CHAR(255) NOT NULL,
    "status" DATE NOT NULL,
    "blogcategory" CHAR(255) NOT NULL,
    "file" CHAR(255) NOT NULL
);
ALTER TABLE
    "Blog" ADD PRIMARY KEY("id");
ALTER TABLE
    "Blog" ADD PRIMARY KEY("user");
ALTER TABLE
    "Blog" ADD PRIMARY KEY("blogcategory");
CREATE TABLE "Ticket"(
    "id" BIGINT NOT NULL,
    "title" CHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "uploaded_by" CHAR(255) NOT NULL,
    "bootcamp" CHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "status" BOOLEAN NOT NULL,
    "slug" CHAR(255) NOT NULL
);
ALTER TABLE
    "Ticket" ADD PRIMARY KEY("id");
ALTER TABLE
    "Ticket" ADD PRIMARY KEY("uploaded_by");
ALTER TABLE
    "Ticket" ADD PRIMARY KEY("bootcamp");
CREATE TABLE "TicketMessage"(
    "id" BIGINT NOT NULL,
    "ticket" CHAR(255) NOT NULL,
    "sender" CHAR(255) NOT NULL,
    "message" TEXT NOT NULL,
    "created_at" DATE NOT NULL,
    "attachment" CHAR(255) NOT NULL,
    "title" CHAR(255) NOT NULL,
    "slug" CHAR(255) NOT NULL
);
ALTER TABLE
    "TicketMessage" ADD PRIMARY KEY("id");
ALTER TABLE
    "TicketMessage" ADD PRIMARY KEY("ticket");
CREATE TABLE "SMSLog"(
    "id" BIGINT NOT NULL,
    "phone_number" CHAR(255) NOT NULL,
    "full_name" CHAR(255) NOT NULL,
    "status" CHAR(255) NOT NULL,
    "response_message" TEXT NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "SMSLog" ADD PRIMARY KEY("id");
ALTER TABLE
    "SMSLog" ADD PRIMARY KEY("full_name");
CREATE TABLE "Invoice"(
    "id" BIGINT NOT NULL,
    "client" CHAR(255) NOT NULL,
    "amount" INTEGER NOT NULL,
    "deadline" DATE NOT NULL,
    "description" TEXT NOT NULL,
    "created_at" DATE NOT NULL,
    "is_paid" BOOLEAN NOT NULL
);
ALTER TABLE
    "Invoice" ADD PRIMARY KEY("id");
ALTER TABLE
    "Invoice" ADD PRIMARY KEY("client");
CREATE TABLE "payment"(
    "id" BIGINT NOT NULL,
    "user" CHAR(255) NOT NULL,
    "invoice" CHAR(255) NOT NULL,
    "method" BOOLEAN NOT NULL,
    "paid_at" DATE NOT NULL,
    "is_verified" BOOLEAN NOT NULL,
    "tracking_code" INTEGER NOT NULL,
    "receipt_image" CHAR(255) NOT NULL,
    "new_column" BIGINT NOT NULL
);
ALTER TABLE
    "payment" ADD PRIMARY KEY("id");
ALTER TABLE
    "payment" ADD PRIMARY KEY("user");
ALTER TABLE
    "payment" ADD PRIMARY KEY("invoice");
CREATE TABLE "Transaction"(
    "id" BIGINT NOT NULL,
    "user" CHAR(255) NOT NULL,
    "amount" INTEGER NOT NULL,
    "description" TEXT NOT NULL,
    "transaction_date" DATE NOT NULL,
    "transaction_type" CHAR(255) NOT NULL,
    "is_verified" BIGINT NOT NULL
);
ALTER TABLE
    "Transaction" ADD PRIMARY KEY("id");
ALTER TABLE
    "Transaction" ADD PRIMARY KEY("user");
CREATE TABLE "wallet"(
    "id" BIGINT NOT NULL,
    "owner" CHAR(255) NOT NULL,
    "balance" INTEGER NOT NULL,
    "date_created" DATE NOT NULL,
    "status" BOOLEAN NOT NULL,
    "updated_at" DATE NOT NULL,
    "new_column" BIGINT NOT NULL
);
ALTER TABLE
    "wallet" ADD PRIMARY KEY("id");
ALTER TABLE
    "wallet" ADD PRIMARY KEY("owner");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "payment"("user");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "Blog"("user");
ALTER TABLE
    "Bootcamp" ADD CONSTRAINT "bootcamp_id_foreign" FOREIGN KEY("id") REFERENCES "BootcampRegistration"("bootcamp");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "Bootcamp"("instructor");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "TicketMessage"("id");
ALTER TABLE
    "BlogCategory" ADD CONSTRAINT "blogcategory_id_foreign" FOREIGN KEY("id") REFERENCES "Blog"("blogcategory");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "BootcampRegistration"("volunteer");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "BootcampRegistration"("reviewed_by");
ALTER TABLE
    "Invoice" ADD CONSTRAINT "invoice_id_foreign" FOREIGN KEY("id") REFERENCES "payment"("invoice");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "wallet"("owner");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "SMSLog"("full_name");
ALTER TABLE
    "BootCampCategory" ADD CONSTRAINT "bootcampcategory_id_foreign" FOREIGN KEY("id") REFERENCES "Bootcamp"("category");
ALTER TABLE
    "Ticket" ADD CONSTRAINT "ticket_id_foreign" FOREIGN KEY("id") REFERENCES "TicketMessage"("ticket");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "Invoice"("client");
ALTER TABLE
    "Account" ADD CONSTRAINT "account_id_foreign" FOREIGN KEY("id") REFERENCES "Transaction"("user");