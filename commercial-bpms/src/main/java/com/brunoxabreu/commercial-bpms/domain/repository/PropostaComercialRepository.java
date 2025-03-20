package com.brunoxabreu.commercial_bpms.domain.repository;

import com.brunoxabreu.commercial_bpms.domain.model.PropostaComercial;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PropostaComercialRepository extends JpaRepository<PropostaComercial, Long> {
    Optional<PropostaComercial> findByNumeroProposta(String numeroProposta);
    Optional<PropostaComercial> findByProcessoInstanceId(String processoInstanceId);
} 