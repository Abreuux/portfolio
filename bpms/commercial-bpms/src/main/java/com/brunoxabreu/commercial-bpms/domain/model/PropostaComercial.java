package com.brunoxabreu.commercial_bpms.domain.model;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "propostas_comerciais")
public class PropostaComercial {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String numeroProposta;

    @Column(nullable = false)
    private String cliente;

    @Column(nullable = false)
    private String vendedor;

    @Column(nullable = false)
    private BigDecimal valorTotal;

    @Column(nullable = false)
    private String status;

    @Column(nullable = false)
    private LocalDateTime dataCriacao;

    private LocalDateTime dataAprovacao;

    private String observacoes;

    @Column(nullable = false)
    private String processoInstanceId;

    @PrePersist
    protected void onCreate() {
        dataCriacao = LocalDateTime.now();
    }
} 