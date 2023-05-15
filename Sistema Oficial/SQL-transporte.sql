CREATE TABLE `motoristas` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    `sobrenome` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    `cpf` VARCHAR(14) NOT NULL COLLATE 'utf8mb4_general_ci',
    `cnh` VARCHAR(11) NOT NULL COLLATE 'utf8mb4_general_ci',
    `modelo_veiculo` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    `placa` VARCHAR(8) NOT NULL COLLATE 'utf8mb4_general_ci',
    `usuario` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    `senha` VARCHAR(64) NOT NULL COLLATE 'utf8mb4_general_ci',
    `status` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_general_ci',
    `salt` VARCHAR(32) NOT NULL COLLATE 'utf8mb4_general_ci',
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `cpf` (`cpf`) USING BTREE,
    UNIQUE INDEX `cnh` (`cnh`) USING BTREE,
    UNIQUE INDEX `placa` (`placa`) USING BTREE,
    UNIQUE INDEX `usuario` (`usuario`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=2
;
