package com.brunoxabreu.lead_enrichment.domain.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.Map;

@Data
@Entity
@Table(name = "leads")
public class Lead {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nome;

    @Column(nullable = false)
    private String email;

    private String empresa;

    private String cargo;

    private String telefone;

    private String linkedinUrl;

    @Column(columnDefinition = "jsonb")
    private Map<String, Object> dadosEnriquecidos;

    @Column(nullable = false)
    private String status;

    @Column(nullable = false)
    private LocalDateTime dataCriacao;

    private LocalDateTime dataEnriquecimento;

    private String observacoes;

    @Column(nullable = false)
    private String processoInstanceId;

    @PrePersist
    protected void onCreate() {
        dataCriacao = LocalDateTime.now();
    }
} 