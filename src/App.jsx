import { useEffect, useRef, useState } from 'react'

const Arrow = ({ diagonal = false }) => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d={diagonal ? 'M7 17 17 7M8 7h9v9' : 'M5 12h14m-5-5 5 5-5 5'} />
  </svg>
)

const Check = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="m5 12 4 4L19 6" />
  </svg>
)

const services = [
  {
    number: '01',
    label: 'Attract leads',
    title: 'Maak van aandacht een voorspelbare instroom.',
    text: 'Van positionering en campagnes tot prospectie. We vullen je pipeline met bedrijven die passen bij je ambitie.',
    accent: 'orange',
  },
  {
    number: '02',
    label: 'Boost sales',
    title: 'Maak van gesprekken gewonnen deals.',
    text: 'We brengen structuur, technologie en commerciële slagkracht samen — en zorgen dat je team ermee werkt.',
    accent: 'blue',
  },
  {
    number: '03',
    label: 'Keep clients',
    title: 'Maak van klanten duurzame groei.',
    text: 'Sterke service en slimme retentie maken bestaande klanten waardevoller. Wij bouwen het proces én voeren het uit.',
    accent: 'sand',
  },
]

const differences = [
  ['Strategie', 'Van plan naar werkend commercieel systeem'],
  ['Uitvoering', '150+ mensen die mee aan de knoppen zitten'],
  ['Verantwoordelijkheid', 'Eén partner over de volledige klantreis'],
  ['Meetlat', 'Geen ijdel rapport. Commerciële vooruitgang.'],
]

const cases = [
  {
    name: 'Orange',
    category: 'Attract leads',
    title: 'Eén team. Eén doel. Constante commerciële beweging.',
    image: '/assets/case-orange.png',
    url: 'https://salesup.be/client-cases/de-3-saleslessen-van-stefanie-van-rillaer-head-of-hunting-bij-orange',
  },
  {
    name: 'Trustteam',
    category: 'Boost sales',
    title: 'Groei versnellen met hetzelfde ondernemende DNA.',
    image: '/assets/case-trustteam.png',
    url: 'https://salesup.be/client-cases/trustteam-x-salesup-groei-versnellen-met-hetzelfde-dna',
  },
  {
    name: 'Liantis',
    category: 'Keep clients',
    title: 'Mensen laten groeien om bedrijven te laten groeien.',
    image: '/assets/case-liantis.png',
    url: 'https://salesup.be/client-cases/liantis-x-salesup-mensen-laten-groeien-om-groei-mogelijk-te-maken',
  },
]

function App() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [activeService, setActiveService] = useState(0)
  const caseRail = useRef(null)

  useEffect(() => {
    const elements = document.querySelectorAll('[data-reveal]')
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add('is-visible')
        })
      },
      { threshold: 0.12 },
    )
    elements.forEach((element) => observer.observe(element))
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    document.body.classList.toggle('menu-open', menuOpen)
    return () => document.body.classList.remove('menu-open')
  }, [menuOpen])

  const scrollCases = (direction) => {
    caseRail.current?.scrollBy({ left: direction * 440, behavior: 'smooth' })
  }

  return (
    <>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="salesUp home">
          <img src="/assets/logo-salesup.svg" alt="salesUp" />
        </a>
        <nav className={menuOpen ? 'nav nav--open' : 'nav'} aria-label="Hoofdnavigatie">
          <a href="#aanpak" onClick={() => setMenuOpen(false)}>Onze aanpak</a>
          <a href="#cases" onClick={() => setMenuOpen(false)}>Cases</a>
          <a href="#over-ons" onClick={() => setMenuOpen(false)}>Over ons</a>
          <a href="#inzichten" onClick={() => setMenuOpen(false)}>Inzichten</a>
        </nav>
        <a className="header-cta" href="#contact">
          Daag ons uit <Arrow diagonal />
        </a>
        <button
          className={menuOpen ? 'menu-button is-active' : 'menu-button'}
          onClick={() => setMenuOpen((current) => !current)}
          aria-expanded={menuOpen}
          aria-label="Menu openen"
        >
          <span />
          <span />
        </button>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-grid" aria-hidden="true" />
          <div className="hero-content">
            <p className="eyebrow eyebrow--light" data-reveal>Commerciële groei, ontworpen om door te gaan.</p>
            <h1 data-reveal>
              Wat je naar <em>5 miljoen</em> bracht, brengt je niet naar 15.
            </h1>
            <div className="hero-bottom" data-reveal>
              <p>
                Je netwerk, sterke verkopers, een bureau erbij: zo groeit elk bedrijf — tot het
                stopt. Voor de volgende sprong heb je geen extra advies nodig, maar een
                commerciële machine.
              </p>
              <a className="circle-link" href="#aanpak" aria-label="Ontdek hoe salesUp werkt">
                <Arrow />
              </a>
            </div>
          </div>
          <div className="hero-stamp" aria-hidden="true">
            <span>WE BUILD</span>
            <b>↑</b>
            <span>WE RUN</span>
          </div>
          <div className="scroll-cue">
            <span />
            Scroll om te groeien
          </div>
        </section>

        <section className="proof-strip" aria-label="salesUp in cijfers">
          <div data-reveal>
            <strong>21</strong>
            <span>jaar commerciële ervaring</span>
          </div>
          <div data-reveal>
            <strong>150+</strong>
            <span>mensen die uitvoeren</span>
          </div>
          <div data-reveal>
            <strong>01</strong>
            <span>partner voor de hele klantreis</span>
          </div>
          <p className="proof-note">Van strategie tot telefoon. Van campagne tot klant.</p>
        </section>

        <section className="manifesto section-shell">
          <p className="eyebrow" data-reveal>De commerciële realiteit</p>
          <div className="manifesto-heading" data-reveal>
            <h2>Advies heb je genoeg gehad.</h2>
            <span className="scribble" aria-hidden="true">Genoeg.</span>
          </div>
          <div className="manifesto-copy" data-reveal>
            <p>
              De strategie ligt er. Het rapport is gelezen. De workshop was inspirerend.
              Ondertussen komt groei nog altijd uit dezelfde drie bronnen als vier jaar geleden.
            </p>
            <p>
              Wij blijven niet aan de zijlijn staan. salesUp bouwt de commerciële motor en zet
              mensen, processen en technologie in beweging. Elke dag opnieuw.
            </p>
          </div>
        </section>

        <section className="services" id="aanpak">
          <div className="section-shell">
            <div className="section-intro" data-reveal>
              <div>
                <p className="eyebrow eyebrow--light">Eén verbonden groeimodel</p>
                <h2>Wij bouwen ze.<br />En wij draaien ze.</h2>
              </div>
              <p>
                Geen verzameling losse diensten. Eén commerciële machine die aandacht omzet in
                gesprekken, gesprekken in klanten en klanten in duurzame groei.
              </p>
            </div>

            <div className="service-tabs" role="tablist" aria-label="Onze aanpak" data-reveal>
              {services.map((service, index) => (
                <button
                  key={service.label}
                  className={activeService === index ? 'service-tab is-active' : 'service-tab'}
                  onClick={() => setActiveService(index)}
                  role="tab"
                  aria-selected={activeService === index}
                >
                  <span>{service.number}</span>
                  {service.label}
                </button>
              ))}
            </div>

            <div className={`service-stage service-stage--${services[activeService].accent}`} data-reveal>
              <div className="service-visual" aria-hidden="true">
                <span className="orbit orbit--one" />
                <span className="orbit orbit--two" />
                <span className="orbit-core">UP</span>
              </div>
              <div className="service-detail">
                <span>{services[activeService].number} / 03</span>
                <h3>{services[activeService].title}</h3>
                <p>{services[activeService].text}</p>
                <a href="#contact">Ontdek deze aanpak <Arrow /></a>
              </div>
            </div>
          </div>
        </section>

        <section className="comparison section-shell">
          <div className="comparison-title" data-reveal>
            <p className="eyebrow">Het verschil zit in eigenaarschap</p>
            <h2>Vier leveranciers.<br />Vier rapporten.</h2>
            <p>Wie is er verantwoordelijk voor je omzet?</p>
          </div>
          <div className="comparison-table" data-reveal>
            <div className="comparison-head">
              <span>Traditioneel</span>
              <span>salesUp</span>
            </div>
            {differences.map(([label, value]) => (
              <div className="comparison-row" key={label}>
                <span><i>×</i>{label} eindigt bij de oplevering</span>
                <span><Check />{value}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="cases" id="cases">
          <div className="cases-head section-shell" data-reveal>
            <div>
              <p className="eyebrow">Werk dat werkt</p>
              <h2>Groei in beweging.</h2>
            </div>
            <div className="rail-controls">
              <button onClick={() => scrollCases(-1)} aria-label="Vorige case"><Arrow /></button>
              <button onClick={() => scrollCases(1)} aria-label="Volgende case"><Arrow /></button>
            </div>
          </div>
          <div className="case-rail" ref={caseRail}>
            {cases.map((item, index) => (
              <article className="case-card" key={item.name} data-reveal>
                <div className="case-image">
                  <img src={item.image} alt="" />
                  <span>{String(index + 1).padStart(2, '0')}</span>
                </div>
                <div className="case-meta">
                  <p>{item.category}</p>
                  <p>{item.name}</p>
                </div>
                <h3>{item.title}</h3>
                <a href={item.url}>Bekijk de case <Arrow diagonal /></a>
              </article>
            ))}
          </div>
        </section>

        <section className="people" id="over-ons">
          <div className="people-image" data-reveal>
            <img src="/assets/team-office.png" alt="salesUp-team aan het werk" />
          </div>
          <div className="people-copy" data-reveal>
            <p className="eyebrow eyebrow--light">Mensen maken de machine</p>
            <h2>Strak op het proces. Warm in de samenwerking.</h2>
            <p>
              Achter elk dashboard staan mensen die bellen, luisteren, challengen en bijsturen.
              Specialisten die je business leren kennen en verantwoordelijkheid nemen alsof ze
              naast je zitten.
            </p>
            <a className="text-link text-link--light" href="#contact">
              Ontmoet de mensen van salesUp <Arrow />
            </a>
          </div>
        </section>

        <section className="insights section-shell" id="inzichten">
          <div className="insights-title" data-reveal>
            <p className="eyebrow">Vooruitkijken</p>
            <h2>Wat morgen verkoopt, moet je vandaag bouwen.</h2>
          </div>
          <div className="insight-list">
            {[
              ['Strategie', 'Waarom je commerciële motor achterloopt op je bedrijf'],
              ['Sales', 'Van een goed team naar een herhaalbaar verkoopproces'],
              ['AI & data', 'Technologie die verkopers sterker maakt, niet drukker'],
            ].map(([tag, title], index) => (
              <a href="#contact" className="insight-row" key={title} data-reveal>
                <span>0{index + 1}</span>
                <p><small>{tag}</small>{title}</p>
                <i><Arrow diagonal /></i>
              </a>
            ))}
          </div>
        </section>

        <section className="contact" id="contact">
          <div className="contact-mark" aria-hidden="true">↑</div>
          <div className="contact-copy" data-reveal>
            <p className="eyebrow eyebrow--light">Klaar voor de volgende sprong?</p>
            <h2>Je ambitie is al groot.<br />Nu je commerciële motor nog.</h2>
            <a href="mailto:info@salesup.be" className="contact-button">
              Daag ons uit <Arrow diagonal />
            </a>
          </div>
        </section>
      </main>

      <footer>
        <div className="footer-top">
          <a className="brand brand--footer" href="#top"><img src="/assets/logo-salesup.svg" alt="salesUp" /></a>
          <p>Volledige commerciële groei.<br />Gebouwd én gedraaid.</p>
          <div className="footer-links">
            <a href="#aanpak">Onze aanpak</a>
            <a href="#cases">Cases</a>
            <a href="#over-ons">Over ons</a>
            <a href="mailto:info@salesup.be">Contact</a>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} salesUp</span>
          <span>Aalst · België</span>
          <a href="#top">Terug naar boven ↑</a>
        </div>
      </footer>
    </>
  )
}

export default App
