<template>
    <header class="header header--4 header--fixed">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <nav class="menu d-lg-flex justify-content-lg-between align-items-lg-center py-3 py-lg-0">
                        <div class="d-flex align-items-center justify-content-between">
                            <a href="index.html" class="logo link d-inline-flex align-items-center flex-shrink-0">
                                <img src="../../../public/img/logo-light.png" alt="logo"
                                    class="img-fluid object-fit-contain" width="150" height="50">
                            </a>
                            <button
                                class="menu-toggle w-15 h-15 p-0 border-0 lh-1 bg-primary-50 clr-neutral-100 :clr-neutral-100 transition :bg-primary-300 rounded flex-shrink-0 d-lg-none order-sm-3 fs-24">
                                <i class="bi bi-list"></i>
                            </button>
                        </div>

                        <div
                            class="menu-nav d-flex align-items-lg-center flex-column flex-lg-row flex-grow-1 gap-4 pb-4 pb-lg-0 rounded">
                            <ul class="list list-lg-row ms-lg-auto align-items-lg-center">
                                <li class="menu-list">
                                    <RouterLink to="/" class="link menu-link"> Home </RouterLink>
                                </li>
                                    <li class="menu-list">
                                        <RouterLink to="/pricing" class="link menu-link"> Pricing </RouterLink>
                                    </li>
                                    <li class="menu-list">
                                        <RouterLink to="/privacy" class="link menu-link"> Privacy </RouterLink>
                                    </li>
                                    <li class="menu-list">
                                        <RouterLink to="/terms" class="link menu-link"> Terms </RouterLink>
                                    </li>
                                
                                
                                <li class="menu-list">
                                    <RouterLink to="/login">
                                        <div
                                            class="link d-inline-flex align-items-center gap-2 py-2 px-3 rounded-1 bg-grad-6 clr-white fw-bold fs-14">
                                            <span class="d-inline-block ff-3"> Get Started </span>
                                            <span class="d-inline-block fs-12">
                                                <i class="bi bi-arrow-up-right"></i>
                                            </span>
                                        </div>

                                    </RouterLink>

                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    </header>
</template>