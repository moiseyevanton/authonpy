CREATE TABLE Employers (
    ID_employer SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE Stores (
    ID_store SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    ID_employer INTEGER NOT NULL,

    FOREIGN KEY (ID_employer) REFERENCES Employers(ID_employer)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE INDEX idx_stores_employer
ON Stores(ID_employer);


CREATE TABLE Administrators (
    ID_administrator SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    ID_employer INTEGER NOT NULL,

    FOREIGN KEY (ID_employer) REFERENCES Employers(ID_employer)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Индекс
CREATE INDEX idx_admin_employer
ON Administrators(ID_employer);


CREATE TABLE Workers (
    ID_worker SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    ID_store INTEGER NOT NULL,
    ID_administrator INTEGER,

    FOREIGN KEY (ID_store) REFERENCES Stores(ID_store)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (ID_administrator) REFERENCES Administrators(ID_administrator)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


CREATE INDEX idx_workers_store
ON Workers(ID_store);

CREATE INDEX idx_workers_admin
ON Workers(ID_administrator);


CREATE TABLE Administrator_Store (
    ID_administrator INTEGER NOT NULL,
    ID_store INTEGER NOT NULL,

    PRIMARY KEY (ID_administrator, ID_store),

    FOREIGN KEY (ID_administrator) REFERENCES Administrators(ID_administrator)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (ID_store) REFERENCES Stores(ID_store)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE INDEX idx_admin_store_admin
ON Administrator_Store(ID_administrator);

CREATE INDEX idx_admin_store_store
ON Administrator_Store(ID_store);


CREATE TABLE UserIPs (
    ID_ip SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    login_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Кто именно заходил (одна из трёх ролей)
    ID_employer INTEGER,
    ID_administrator INTEGER,
    ID_worker INTEGER,

    FOREIGN KEY (ID_employer) REFERENCES Employers(ID_employer)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (ID_administrator) REFERENCES Administrators(ID_administrator)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (ID_worker) REFERENCES Workers(ID_worker)
        ON DELETE CASCADE ON UPDATE CASCADE,

    -- Только один из трёх ID должен быть заполнен
    CONSTRAINT chk_one_user CHECK (
        (ID_employer IS NOT NULL AND ID_administrator IS NULL AND ID_worker IS NULL) OR
        (ID_employer IS NULL AND ID_administrator IS NOT NULL AND ID_worker IS NULL) OR
        (ID_employer IS NULL AND ID_administrator IS NULL AND ID_worker IS NOT NULL)
    )
);

CREATE INDEX idx_user_ips_employer ON UserIPs(ID_employer);
CREATE INDEX idx_user_ips_administrator ON UserIPs(ID_administrator);
CREATE INDEX idx_user_ips_worker ON UserIPs(ID_worker);
CREATE INDEX idx_user_ips_time ON UserIPs(login_time);