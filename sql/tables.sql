-- cadastrame.resources definition

-- Drop table

-- DROP TABLE cadastrame.resources;

CREATE TABLE cadastrame.resources (
	id serial4 NOT NULL,
	page_code varchar(50) NOT NULL,
	form_code varchar(50) NULL,
	description varchar(100) NOT NULL,
	CONSTRAINT resources_pkey PRIMARY KEY (id),
	CONSTRAINT uq_resource UNIQUE (page_code, form_code)
);

-- cadastrame.roles definition

-- Drop table

-- DROP TABLE cadastrame.roles;

CREATE TABLE cadastrame.roles (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	description varchar(255) NULL,
	is_manager bool DEFAULT false NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT roles_name_key UNIQUE (name),
	CONSTRAINT roles_pkey PRIMARY KEY (id)
);

-- cadastrame.rolespermissions definition

-- Drop table

-- DROP TABLE cadastrame.rolespermissions;

CREATE TABLE cadastrame.rolespermissions (
	role_id int4 NOT NULL,
	resource_id int4 NOT NULL,
	CONSTRAINT role_resources_pkey PRIMARY KEY (role_id, resource_id)
);


-- cadastrame.rolespermissions foreign keys

ALTER TABLE cadastrame.rolespermissions ADD CONSTRAINT fk_role_resources_resource FOREIGN KEY (resource_id) REFERENCES cadastrame.resources(id) ON DELETE CASCADE;
ALTER TABLE cadastrame.rolespermissions ADD CONSTRAINT fk_role_resources_role FOREIGN KEY (role_id) REFERENCES cadastrame.roles(id) ON DELETE CASCADE;

-- cadastrame.users definition

-- Drop table

-- DROP TABLE cadastrame.users;

CREATE TABLE cadastrame.users (
	iduser bigserial NOT NULL,
	idrole int2 DEFAULT 1 NOT NULL,
	active bool DEFAULT true NOT NULL,
	username varchar(50) NOT NULL,
	email varchar(255) NOT NULL,
	"password" varchar(255) NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	deactivated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT uk_user_account_username UNIQUE (username),
	CONSTRAINT users_pkey PRIMARY KEY (iduser)
);