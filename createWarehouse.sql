DROP DATABASE IF EXISTS tiki_warehouse;
CREATE DATABASE tiki_warehouse;
USE tiki_warehouse;

DROP TABLE IF EXISTS tiki_warehouse.`Sale_Fact`;  
DROP TABLE IF EXISTS tiki_warehouse.`Time_Dim`;  
DROP TABLE IF EXISTS tiki_warehouse.`Customer_Dim`;
DROP TABLE IF EXISTS tiki_warehouse.`Seller_Dim`; 
DROP TABLE IF EXISTS tiki_warehouse.`Product_Dim`; 
DROP TABLE IF EXISTS tiki_warehouse.`Category_Dim`;

CREATE TABLE tiki_warehouse.`Category_Dim` (
  CategoryID INT NOT NULL,
  Name VARCHAR(100) NOT NULL,
  CategoryPath VARCHAR(200) NOT NULL,
  PRIMARY KEY (CategoryID)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE tiki_warehouse.`Seller_Dim` (
  SellerID INT NOT NULL,
  Name VARCHAR(100) NOT NULL,
  Rating FLOAT NOT NULL,
  Follow INT NOT NULL,
  PRIMARY KEY (SellerID)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE tiki_warehouse.`Customer_Dim` (
  CustomerID INT NOT NULL,
  Name VARCHAR(100) NOT NULL,
  Address VARCHAR(200) NOT NULL,
  PRIMARY KEY (CustomerID)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE tiki_warehouse.`Time_Dim` (
  TimeID INT NOT NULL,
  Date DATETIME NOT NULL,
  Month INT NOT NULL,
  Quarter INT NOT NULL,
  Year INT NOT NULL,
  PRIMARY KEY (TimeID)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE tiki_warehouse.`Product_Dim` (
  ProductID INT NOT NULL,
  CategoryID INT NOT NULL,
  Name VARCHAR(500) NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  Rating FLOAT NOT NULL,
  ReviewCount INT NOT NULL,
  PRIMARY KEY (ProductID),
  CONSTRAINT CategoryRef
    FOREIGN KEY (CategoryID)
    REFERENCES tiki_warehouse.`Category_Dim` (CategoryID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE tiki_warehouse.`Sale_Fact` (
  OrderID INT NOT NULL,
  ProductID INT NOT NULL,
  TimeID INT NOT NULL,
  CustomerID INT NOT NULL,
  SellerID INT NOT NULL,
  Total DECIMAL(10,2) NOT NULL,
  Quantity INT NOT NULL,
  PRIMARY KEY (OrderID, ProductID, TimeID, CustomerID, SellerID),
  CONSTRAINT ProductRef
    FOREIGN KEY (ProductID)
    REFERENCES tiki_warehouse.`Product_Dim` (ProductID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT TimeRef
    FOREIGN KEY (TimeID)
    REFERENCES tiki_warehouse.`Time_Dim` (TimeID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT CustomerRef
    FOREIGN KEY (CustomerID)
    REFERENCES tiki_warehouse.`Customer_Dim` (CustomerID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT SellerRef
    FOREIGN KEY (SellerID)
    REFERENCES tiki_warehouse.`Seller_Dim` (SellerID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB CHARSET=utf8;