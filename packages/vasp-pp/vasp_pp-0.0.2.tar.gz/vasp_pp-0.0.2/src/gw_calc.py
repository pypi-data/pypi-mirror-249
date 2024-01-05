import numpy as np


class GwCalc:

    """
    class GwCalc gets all GW data
    """

    def __init__(
        self,
        finite_temp=None,
        full_freq=None,
        Te=None,
        nbands=None,
        nbandsgw=None,
        nkpts=None,
        nkdim=None,
        nomega=None,
        cshift=None,
        Ef=None,
        band_num=None,
        qp_E=None,
        V_xc=None,
        V_pw_x=None,
        Z=None,
        KS_energies=None,
        sigma=None,
        qp_linear_E=None,
        Z_linear=None,
        qp_zeros_E=None,
        Z_zeros=None,
        occ=None,
        imag_self_energy=None,
        qp_diff=None,
        tag=None,
        ff_freq_grid=None,
        ff_re_self_energy=None,
        ff_im_self_energy=None,
    ) -> None:
        """
        Function returns all important data from various GW calculations as attributes


        Args:
            finite_temp (string): GW calculation type (T/F). Defaults to None.
            full_freq (string): GW calculation type (T/F). Defaults to None.
            Te (float): Electronic temperature in eV. Defaults to None.
            nbands (int): Number of bands in calculation. Defaults to None.
            nbandsgw (int): Number of bands included in GW calculation. Defaults to None.
            nkpts (int): Number of irreducible kpoints in calculation. Defaults to None.
            nkdim (int): Total number of kpoints in calculation. Defaults to None.
            nomega (int): Number of frequency grid points in GW calculation. Defaults to None.
            cshift (float): Shift of the Hilbert transformation for GW calculation. Defaults to None.
            Ef (float): Fermi energy of calculation. Defaults to None.
            band_num (array): (finite/zero, non-FF) GW data output band number label. Defaults to None.
            qp_E (array): (zero,non-FF) GW data output Quasi-particle energy. Defaults to None.
            V_xc (array): (zero, non-FF) GW data output V_xc. Defaults to None.
            V_pw_x (array): (zero, non-FF) GW data output V_pw_x. Defaults to None.
            Z (array): (zero, non-FF) GW data output Z. Defaults to None.
            KS_energies (array): (finite/zero, non-FF) GW data output Kohn-Sham energies. Defaults to None.
            sigma (array): (finite/zero, non-FF) GW data output sigma. Defaults to None.
            qp_linear_E (array): (finite, non-FF) GW data output quasi-particle energies for linear method. Defaults to None.
            Z_linear (array): (finite, non-FF) GW data output Z for linear method. Defaults to None.
            qp_zeros_E (array): (finite, non-FF) GW data output quasi-particle energies for zeros method. Defaults to None.
            Z_zeros (array): (finite, non-FF) GW data output Z for zeros method. Defaults to None.
            occ (array): (finite/zero, non-FF) GW data output for nk state occupations. Defaults to None.
            imag_self_energy (array): (finite/zero, non-FF) GW data output of the imaginary part of the self-energy. Defaults to None.
            qp_diff (array): (finite, non-FF) GW data output of linear and zero method quais-particle energy difference. Defaults to None.
            tag (array): (finite, non-FF) GW data output for tag. Defaults to None.
            ff_freq_grid (array): (zero, FF) GW data output of full-frequency grid. Defaults to None.
            ff_re_self_energy (array): (zero, FF) GW data output of frequency-dependent real part of the self-energy. Defaults to None.
            ff_im_self_energy (array): (zero, FF) GW data output of frequency-dependent imaginary part of the self-energy. Defaults to None.
        """
        self.finite_temp = finite_temp
        self.full_freq = full_freq
        self.Te = Te
        self.nbands = nbands
        self.nbandsgw = nbandsgw
        self.nkpts = nkpts
        self.nkdim = nkdim
        self.nomega = nomega
        self.cshift = cshift
        self.Ef = Ef
        self.band_num = band_num
        self.qp_E = qp_E
        self.V_xc = V_xc
        self.V_pw_x = V_pw_x
        self.Z = Z
        self.KS_energies = KS_energies
        self.sigma = sigma
        self.qp_linear_E = qp_linear_E
        self.Z_linear = Z_linear
        self.qp_zeros_E = qp_zeros_E
        self.Z_zeros = Z_zeros
        self.occ = occ
        self.imag_self_energy = imag_self_energy
        self.qp_diff = qp_diff
        self.tag = tag
        self.ff_freq_grid = ff_freq_grid
        self.ff_re_self_energy = ff_re_self_energy
        self.ff_im_self_energy = ff_im_self_energy


def get_full_freq_self_energy(outcar, nkpts, nbandsgw):
    """Function obtains freq. values and self-energies for full-frequency GW calculation within the zero-temperature formalism

    Args:
        outcar (string): VASP OUTCAR file name
        nkpts (int): Number of irreducible k-points used in VASP calculation
        nbandsgw (int): Number of bands used in GW VASP calculation

    Returns:
        ff_freq_grid (array): GW data output of full-frequency grid.
        ff_re_self_energy (array): GW data output of frequency-dependent real part of the self-energy.
        ff_im_self_energy (array): GW data output of frequency-dependent imaginary part of the self-energy.
    """
    ncol = 3
    match_string = (
        "calculating selfenergy CALC_SELFENERGY_LINEAR between w= -50.00  50.00"
    )
    file = [line for line in open(outcar, "r")]
    header_num = [
        line_num for line_num, line in enumerate(file) if match_string in line
    ][0]

    ff_data = file[header_num:]
    ff_data_clean = (
        np.array(
            [
                [
                    x.split()
                    for x in [x.strip() for x in ff_data if len(x.split()) == ncol]
                ]
            ]
        )
        .flatten()
        .astype(float)
    )

    ff_freq_grid = ff_data_clean[0::ncol].reshape(
        nkpts, nbandsgw, int(len(ff_data_clean) / nkpts / nbandsgw / ncol)
    )
    ff_re_self_energy = ff_data_clean[1::ncol].reshape(
        nkpts, nbandsgw, int(len(ff_data_clean) / nkpts / nbandsgw / ncol)
    )
    ff_im_self_energy = ff_data_clean[2::ncol].reshape(
        nkpts, nbandsgw, int(len(ff_data_clean) / nkpts / nbandsgw / ncol)
    )
    return ff_freq_grid, ff_re_self_energy, ff_im_self_energy


def get_finite_Te_self_energy(outcar, nkpts):
    """Function obtains key output values from a finite-temperature GW calculation

    Args:
        outcar (string): VASP OUTCAR file name
        nkpts (int): Number of irreducible k-points used in the VASP calculation

    Returns:
        band_num (array): GW data output band number label. Defaults to None.
        KS_energies (array): GW data output Kohn-Sham energies. Defaults to None.
        sigma (array): GW data output sigma. Defaults to None.
        qp_linear_E (array): GW data output quasi-particle energies for linear method. Defaults to None.
        Z_linear (array): GW data output Z for linear method. Defaults to None.
        qp_zeros_E (array): GW data output quasi-particle energies for zeros method. Defaults to None.
        Z_zeros (array): GW data output Z for zeros method. Defaults to None.
        occ (array): GW data output for nk state occupations. Defaults to None.
        imag_self_energy (array): GW data output of the imaginary part of the self-energy. Defaults to None.
        qp_diff (array): GW data output of linear and zero method quais-particle energy difference. Defaults to None.
        tag (array): GW data output for tag. Defaults to None.
    """

    ncol = 11
    match_string = "QP shifts evaluated in KS"
    file = [line for line in open(outcar, "r")]
    header_num = [
        line_num for line_num, line in enumerate(file) if match_string in line
    ][0]

    finite_data = file[header_num:]

    finite_data_clean = (
        np.array(
            [
                [
                    x.split()
                    for x in [x.strip() for x in finite_data if len(x.split()) == ncol]
                ]
            ]
        )
        .flatten()
        .astype(float)
    )

    nbands = int(len(finite_data_clean) / (nkpts * ncol))

    band_num = finite_data_clean[0::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    KS_energies = finite_data_clean[1::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    sigma = finite_data_clean[2::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    qp_linear_E = finite_data_clean[3::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    Z_linear = finite_data_clean[4::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    qp_zeros_E = finite_data_clean[5::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    Z_zeros = finite_data_clean[6::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    occ = finite_data_clean[7::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    imag_self_energy = finite_data_clean[8::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    qp_diff = finite_data_clean[9::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )
    tag = finite_data_clean[10::ncol].reshape(
        nkpts, nbands, int(len(finite_data_clean) / nkpts / nbands / ncol)
    )

    return (
        band_num,
        KS_energies,
        sigma,
        qp_linear_E,
        Z_linear,
        qp_zeros_E,
        Z_zeros,
        occ,
        imag_self_energy,
        qp_diff,
        tag,
    )


def get_zero_self_energy(outcar, nkpts, nbands):
    """Function obtains key output values from a (non-FF) zero-temperature GW calculation

    Args:
        outcar (string): VASP OUTCAR file name
        nkpts (int): Number of irreducible k-points used in the VASP calculation
        nbands (int): Number of bands used in the VASP calculation

    Returns:
        band_num (array): GW data output band number label. Defaults to None.
        qp_E (array): GW data output Quasi-particle energy. Defaults to None.
        V_xc (array): GW data output V_xc. Defaults to None.
        V_pw_x (array): GW data output V_pw_x. Defaults to None.
        Z (array): GW data output Z. Defaults to None.
        KS_energies (array): GW data output Kohn-Sham energies. Defaults to None.
        sigma (array): GW data output sigma. Defaults to None.
        occ (array): GW data output for nk state occupations. Defaults to None.
        imag_self_energy (array): GW data output of the imaginary part of the self-energy. Defaults to None.
    """
    ncol = 9
    head_match_string = "QP shifts <psi_nk|"
    file = [line for line in open(outcar, "r")]
    header_num = [
        line_num for line_num, line in enumerate(file) if head_match_string in line
    ][0] + 2
    tail_match_string = "QP_SHIFT:  cpu time"
    tail_num = [
        line_num for line_num, line in enumerate(file) if tail_match_string in line
    ][0]

    zero_data = file[header_num:tail_num]
    zero_data_clean = (
        np.array(
            [
                [
                    x.split()
                    for x in [x.strip() for x in zero_data if len(x.split()) == ncol]
                ]
            ]
        )
        .flatten()
        .astype(float)
    )

    band_num = zero_data_clean[0::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    KS_energies = zero_data_clean[1::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    qp_E = zero_data_clean[2::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    sigma = zero_data_clean[3::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    V_xc = zero_data_clean[4::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    V_pw_x = zero_data_clean[5::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    Z = zero_data_clean[6::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    occ = zero_data_clean[7::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )
    imag_self_energy = zero_data_clean[8::ncol].reshape(
        nkpts, nbands, int(len(zero_data_clean) / nkpts / nbands / ncol)
    )

    return band_num, KS_energies, qp_E, sigma, V_xc, V_pw_x, Z, occ, imag_self_energy


def get_params(outcar):
    """Function reads through VASP output file (OUTCAR) and parses out key parameters
       Function then calls proper GW function to parse GW data

    Args:
        outcar (string): VASP OUTCAR file name

    Returns:
        finite_temp (string): GW calculation type (T/F). Defaults to None.
        full_freq (string): GW calculation type (T/F). Defaults to None.
        Te (float): Electronic temperature in eV. Defaults to None.
        nbands (int): Number of bands in calculation. Defaults to None.
        nbandsgw (int): Number of bands included in GW calculation. Defaults to None.
        nkpts (int): Number of irreducible kpoints in calculation. Defaults to None.
        nkdim (int): Total number of kpoints in calculation. Defaults to None.
        nomega (int): Number of frequency grid points in GW calculation. Defaults to None.
        cshift (float): Shift of the Hilbert transformation for GW calculation. Defaults to None.
        Ef (float): Fermi energy of calculation. Defaults to None.
        band_num (array): (finite/zero, non-FF) GW data output band number label. Defaults to None.
        qp_E (array): (zero,non-FF) GW data output Quasi-particle energy. Defaults to None.
        V_xc (array): (zero, non-FF) GW data output V_xc. Defaults to None.
        V_pw_x (array): (zero, non-FF) GW data output V_pw_x. Defaults to None.
        Z (array): (zero, non-FF) GW data output Z. Defaults to None.
        KS_energies (array): (finite/zero, non-FF) GW data output Kohn-Sham energies. Defaults to None.
        sigma (array): (finite/zero, non-FF) GW data output sigma. Defaults to None.
        qp_linear_E (array): (finite, non-FF) GW data output quasi-particle energies for linear method. Defaults to None.
        Z_linear (array): (finite, non-FF) GW data output Z for linear method. Defaults to None.
        qp_zeros_E (array): (finite, non-FF) GW data output quasi-particle energies for zeros method. Defaults to None.
        Z_zeros (array): (finite, non-FF) GW data output Z for zeros method. Defaults to None.
        occ (array): (finite/zero, non-FF) GW data output for nk state occupations. Defaults to None.
        imag_self_energy (array): (finite/zero, non-FF) GW data output of the imaginary part of the self-energy. Defaults to None.
        qp_diff (array): (finite, non-FF) GW data output of linear and zero method quais-particle energy difference. Defaults to None.
        tag (array): (finite, non-FF) GW data output for tag. Defaults to None.
        ff_freq_grid (array): (zero, FF) GW data output of full-frequency grid. Defaults to None.
        ff_re_self_energy (array): (zero, FF) GW data output of frequency-dependent real part of the self-energy. Defaults to None.
        ff_im_self_energy (array): (zero, FF) GW data output of frequency-dependent imaginary part of the self-energy. Defaults to None.
    """

    file = [line for line in open(outcar, "r")]
    finite_temp = [line for line in file if "LFINITE_T" in line][-1].split()[-5]
    full_freq = [line for line in file if "LSELFENERGY" in line][-1].split()[-7]
    # use Te instead of sigma due to sigma being used for self-energy elsewhere
    Te = float([line for line in file if "SIGMA" in line][0].split()[-1])
    Ef = float([line for line in file if "E-fermi" in line][0].split()[-1])
    nbands = int([line for line in file if "NBANDS" in line][0].split()[-1])
    nbandsgw = int([line for line in file if "NBANDSGW " in line][-1].split()[-10])
    nkpts = int([line for line in file if "NKPTS" in line][0].split()[3])
    nkdim = int([line for line in file if "NKDIM" in line][0].split()[9])
    nomega = int([line for line in file if "NOMEGA" in line][0].split()[-1])
    cshift = float([line for line in file if "CSHIFT" in line][-1].split()[-9])

    if full_freq == "T":
        ff_freq_grid, ff_re_self_energy, ff_im_self_energy = get_full_freq_self_energy(
            outcar, nkpts, nbandsgw
        )
        return GwCalc(
            finite_temp=finite_temp,
            full_freq=full_freq,
            Te=Te,
            Ef=Ef,
            nbands=nbands,
            nbandsgw=nbandsgw,
            nkpts=nkpts,
            nkdim=nkdim,
            nomega=nomega,
            cshift=cshift,
            ff_freq_grid=ff_freq_grid,
            ff_re_self_energy=ff_re_self_energy,
            ff_im_self_energy=ff_im_self_energy,
        )
    elif finite_temp == "T":
        (
            band_num,
            KS_energies,
            sigma,
            qp_linear_E,
            Z_linear,
            qp_zeros_E,
            Z_zeros,
            occ,
            imag_self_energy,
            qp_diff,
            tag,
        ) = get_finite_Te_self_energy(outcar, nkpts)
        return GwCalc(
            finite_temp=finite_temp,
            full_freq=full_freq,
            Te=Te,
            Ef=Ef,
            nbands=nbands,
            nbandsgw=nbandsgw,
            nkpts=nkpts,
            nkdim=nkdim,
            nomega=nomega,
            cshift=cshift,
            band_num=band_num,
            KS_energies=KS_energies,
            sigma=sigma,
            qp_linear_E=qp_linear_E,
            Z_linear=Z_linear,
            qp_zeros_E=qp_zeros_E,
            Z_zeros=Z_zeros,
            occ=occ,
            imag_self_energy=imag_self_energy,
            qp_diff=qp_diff,
            tag=tag,
        )
    elif finite_temp == "F" and full_freq == "F":
        (
            band_num,
            KS_energies,
            qp_E,
            sigma,
            V_xc,
            V_pw_x,
            Z,
            occ,
            imag_self_energy,
        ) = get_zero_self_energy(outcar, nkpts, nbands)
        return GwCalc(
            finite_temp=finite_temp,
            full_freq=full_freq,
            Te=Te,
            Ef=Ef,
            nbands=nbands,
            nbandsgw=nbandsgw,
            nkpts=nkpts,
            nkdim=nkdim,
            nomega=nomega,
            cshift=cshift,
            band_num=band_num,
            KS_energies=KS_energies,
            sigma=sigma,
            qp_E=qp_E,
            V_xc=V_xc,
            V_pw_x=V_pw_x,
            Z=Z,
            occ=occ,
            imag_self_energy=imag_self_energy,
        )


def get_gw_data(file):
    """Function reads in name of OUTCAR file

    Args:
        file (string): Name of VASP output file - likely of OUTCAR file

    Returns:
        values from get_params function
    """
    return get_params(file)
